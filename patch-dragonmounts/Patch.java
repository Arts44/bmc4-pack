import jdk.internal.org.objectweb.asm.*;
import java.nio.file.*;

/**
 * Injecte une probabilité dans CrossBreedingManager.getCrossBreed.
 *
 *   if (Math.random() < CHANCE) -> comportement d'origine (hybride)
 *   sinon                       -> return null
 *
 * Renvoyer null n'est PAS un cas d'erreur : c'est la valeur que la
 * méthode rend déjà quand la paire n'est pas dans la table, et
 * TameableDragon.spawnChildFromBreeding la traite en retombant sur
 * son propre pile ou face entre les deux parents. On ne crée donc
 * aucun chemin d'exécution neuf — on réemprunte celui du mod.
 */
public class Patch {
    static final String OWNER = "com/github/kay9/dragonmounts/data/CrossBreedingManager";
    static final String BREED = "com/github/kay9/dragonmounts/dragon/breed/DragonBreed";
    static final String NAME  = "getCrossBreed";
    static final String DESC  = "(L" + BREED + ";L" + BREED + ";Lnet/minecraft/core/RegistryAccess;)L" + BREED + ";";

    public static void main(String[] a) throws Exception {
        Path in = Path.of(a[0]), out = Path.of(a[1]);
        double chance = Double.parseDouble(a[2]);

        ClassReader cr = new ClassReader(Files.readAllBytes(in));
        // ClassWriter(0) : on ne recalcule NI les frames NI les maxs.
        // COMPUTE_FRAMES exigerait de charger les classes Minecraft
        // référencées, qui ne sont pas au classpath — il échouerait.
        ClassWriter cw = new ClassWriter(0);

        final boolean[] touche = { false };

        cr.accept(new ClassVisitor(Opcodes.ASM9, cw) {
            @Override
            public MethodVisitor visitMethod(int acc, String n, String d, String sig, String[] ex) {
                MethodVisitor mv = super.visitMethod(acc, n, d, sig, ex);
                if (!NAME.equals(n) || !DESC.equals(d)) return mv;
                touche[0] = true;

                return new MethodVisitor(Opcodes.ASM9, mv) {
                    @Override
                    public void visitCode() {
                        super.visitCode();
                        Label suite = new Label();
                        visitMethodInsn(Opcodes.INVOKESTATIC, "java/lang/Math", "random", "()D", false);
                        visitLdcInsn(chance);
                        visitInsn(Opcodes.DCMPL);          // random < chance -> -1
                        visitJumpInsn(Opcodes.IFLT, suite); // ... donc on garde l'hybride
                        visitInsn(Opcodes.ACONST_NULL);
                        visitInsn(Opcodes.ARETURN);
                        visitLabel(suite);
                        // Frame explicite sur la cible du saut : locals
                        // inchangés, pile vide. Sans elle, le vérifieur
                        // refuse la classe (StackMapTable obligatoire
                        // depuis la version 50).
                        visitFrame(Opcodes.F_NEW, 4,
                            new Object[] { OWNER, BREED, BREED, "net/minecraft/core/RegistryAccess" },
                            0, new Object[0]);
                    }

                    @Override
                    public void visitMaxs(int maxStack, int maxLocals) {
                        // Le prologue empile deux double = 4 cases.
                        super.visitMaxs(Math.max(maxStack, 4), maxLocals);
                    }
                };
            }
        }, ClassReader.EXPAND_FRAMES);

        if (!touche[0]) throw new IllegalStateException("methode " + NAME + DESC + " introuvable");
        Files.write(out, cw.toByteArray());
        System.out.println("patche : chance = " + chance);
    }
}
