import jdk.internal.org.objectweb.asm.*;
import java.io.*;
import java.nio.file.*;
import java.util.zip.*;

/**
 * Patche le jar dragonmounts pour BMC4. Deux corrections.
 *
 * 1) CrossBreedingManager.getCrossBreed — probabilité sur les hybrides.
 *    Prologue : si Math.random() >= CHANCE, on rend null. null n'est pas
 *    un cas d'erreur : c'est déjà ce que la méthode rend quand la paire
 *    n'est pas dans la table, et TameableDragon.spawnChildFromBreeding le
 *    traite en retombant sur son pile ou face entre les deux parents.
 *
 * 2) WitherBreathBall — empêcher la persistance.
 *    Ce souffle est le SEUL des six à ne pas avoir de type d'entité
 *    enregistré : il hérite de WitherSkull et sort donc en jeu comme un
 *    minecraft:wither_skull vanilla. Quand un chunk est sauvegardé puis
 *    rechargé, le jeu reconstruit l'entité depuis son type ENREGISTRÉ —
 *    un WitherSkull vanilla, qui n'a ni la limite de 40 blocs codée dans
 *    le tick() du mod, ni aucun minuteur. La tête devient éternelle.
 *
 *    On ajoute save(CompoundTag) -> false. EntityStorage.storeEntities
 *    appelle Entity.m_20223_ et n'écrit l'entité que s'il rend true
 *    (vérifié dans le jar client de Forge 47.4.20) : le projectile n'est
 *    donc jamais écrit sur disque, et ne peut plus revenir orphelin.
 *
 *    On NE crée PAS de type d'entité dédié, qui serait pourtant la
 *    correction « propre » : les clients tournent avec le jar d'origine
 *    et ne connaîtraient pas ce type, le paquet d'apparition échouerait
 *    chez eux. Ce patch doit rester purement serveur.
 */
public class PatchJar {
    static final String XBREED = "com/github/kay9/dragonmounts/data/CrossBreedingManager";
    static final String BREED  = "com/github/kay9/dragonmounts/dragon/breed/DragonBreed";
    static final String WBB    = "com/github/kay9/dragonmounts/dragon/WitherBreathBall";
    static final String GET_XB = "getCrossBreed";
    static final String GET_XB_DESC =
        "(L" + BREED + ";L" + BREED + ";Lnet/minecraft/core/RegistryAccess;)L" + BREED + ";";
    static final String SAVE      = "m_20223_";            // Entity.save(CompoundTag)
    static final String SAVE_DESC = "(Lnet/minecraft/nbt/CompoundTag;)Z";

    static boolean chanceOk = false, saveOk = false;

    public static void main(String[] a) throws Exception {
        Path in = Path.of(a[0]), out = Path.of(a[1]);
        double chance = Double.parseDouble(a[2]);

        try (ZipFile zf = new ZipFile(in.toFile());
             ZipOutputStream zo = new ZipOutputStream(Files.newOutputStream(out))) {
            var e = zf.entries();
            while (e.hasMoreElements()) {
                ZipEntry src = e.nextElement();
                byte[] data = zf.getInputStream(src).readAllBytes();
                String n = src.getName();
                if (n.equals(XBREED + ".class")) data = patchChance(data, chance);
                else if (n.equals(WBB + ".class")) data = patchNoSave(data);

                ZipEntry dst = new ZipEntry(n);
                dst.setTime(src.getTime());
                dst.setMethod(src.getMethod());
                if (src.getMethod() == ZipEntry.STORED) {
                    dst.setSize(data.length); dst.setCompressedSize(data.length);
                    CRC32 c = new CRC32(); c.update(data); dst.setCrc(c.getValue());
                }
                zo.putNextEntry(dst); zo.write(data); zo.closeEntry();
            }
        }
        if (!chanceOk) throw new IllegalStateException(GET_XB + " introuvable");
        if (!saveOk)   throw new IllegalStateException(WBB + " introuvable");
        System.out.println("OK — chance=" + chance + ", WitherBreathBall non persistant");
    }

    static byte[] patchChance(byte[] b, double chance) {
        ClassReader cr = new ClassReader(b);
        // ClassWriter(0) : ni frames ni maxs recalculés. COMPUTE_FRAMES
        // exigerait de charger les classes Minecraft référencées, qui ne
        // sont pas au classpath.
        ClassWriter cw = new ClassWriter(0);
        cr.accept(new ClassVisitor(Opcodes.ASM9, cw) {
            @Override public MethodVisitor visitMethod(int ac, String n, String d, String s, String[] x) {
                MethodVisitor mv = super.visitMethod(ac, n, d, s, x);
                if (!GET_XB.equals(n) || !GET_XB_DESC.equals(d)) return mv;
                chanceOk = true;
                return new MethodVisitor(Opcodes.ASM9, mv) {
                    @Override public void visitCode() {
                        super.visitCode();
                        Label suite = new Label();
                        visitMethodInsn(Opcodes.INVOKESTATIC, "java/lang/Math", "random", "()D", false);
                        visitLdcInsn(chance);
                        visitInsn(Opcodes.DCMPL);            // random < chance -> -1
                        visitJumpInsn(Opcodes.IFLT, suite);  // ... on garde l'hybride
                        visitInsn(Opcodes.ACONST_NULL);
                        visitInsn(Opcodes.ARETURN);
                        visitLabel(suite);
                        // Frame obligatoire sur la cible du saut.
                        visitFrame(Opcodes.F_NEW, 4,
                            new Object[]{XBREED, BREED, BREED, "net/minecraft/core/RegistryAccess"},
                            0, new Object[0]);
                    }
                    @Override public void visitMaxs(int st, int lo) {
                        super.visitMaxs(Math.max(st, 4), lo); // deux double empilés
                    }
                };
            }
        }, ClassReader.EXPAND_FRAMES);
        return cw.toByteArray();
    }

    static byte[] patchNoSave(byte[] b) {
        ClassReader cr = new ClassReader(b);
        ClassWriter cw = new ClassWriter(0);
        cr.accept(new ClassVisitor(Opcodes.ASM9, cw) {
            boolean deja = false;
            @Override public MethodVisitor visitMethod(int ac, String n, String d, String s, String[] x) {
                if (SAVE.equals(n) && SAVE_DESC.equals(d)) deja = true;
                return super.visitMethod(ac, n, d, s, x);
            }
            @Override public void visitEnd() {
                if (!deja) {
                    MethodVisitor mv = cv.visitMethod(Opcodes.ACC_PUBLIC, SAVE, SAVE_DESC, null, null);
                    mv.visitCode();
                    mv.visitInsn(Opcodes.ICONST_0);
                    mv.visitInsn(Opcodes.IRETURN);
                    mv.visitMaxs(1, 2);
                    mv.visitEnd();
                }
                saveOk = true;
                super.visitEnd();
            }
        }, 0);
        return cw.toByteArray();
    }
}
