# HOMOTOPY THEORETIC MODELS OF IDENTITY TYPES

STEVE AWODEY AND MICHAEL A. WARREN

## 1. Introduction

Quillen [16] introduced model categories as an abstract framework for homotopy theory which would apply to a wide range of mathematical settings. By all accounts this program has been a success and—as, e.g., the work of Voevodsky on the homotopy theory of schemes [14] or the work of Joyal [10, 11] and Lurie [12] on quasicategories seems to indicate—it will likely continue to facilitate mathematical advances. In this paper we present a novel connection between model categories and mathematical logic, inspired by the groupoid model of (intensional) Martin-Löf type theory [13] due to Hofmann and Streicher [8]. In particular, we show that a form of Martin-Löf type theory can be soundly modelled in any model category. This result indicates moreover that any model category has an associated “internal language” which is itself a form of Martin-Löf type theory. This suggests applications both to type theory and to homotopy theory. Because Martin-Löf type theory is, in one form or another, the theoretical basis for many of the computer proof assistants currently in use, such as Coq and Agda (cf. [2] and [4]), this promise of applications is of a practical, as well as theoretical, nature.

The present paper provides a precise indication of this connection between homotopy theory and logic; a more detailed discussion of these and further results will be given in [19].

## 2. Type Theory

Type theory is concerned with (at least) two basic kinds of entities: types and terms. Types are written as $A, B, \ldots$ and terms as $a, b, \ldots$. Every term has a unique type and we write $a : A$ to indicate that a is a term of type A. Types can be thought of as sets and terms as elements of sets or, respectively, as objects of a category and global sections thereof. Alternatively, under an interpretation known as the Curry-Howard correspondence (cf. [15]), a type A can be regarded as a proposition and a term $a : A$ as a proof of A.

The simply typed λ-calculus is the type theory obtained by admitting the construction of products $( A \times B )$ and exponentials (function spaces) $( A \to B )$ of types A and B. Under the Curry-Howard correspondence, the simply typed λ-calculus describes the behavior of proofs in propositional (intuitionistic) logic: $( A \times B )$ is the conjunction $( A \land B )$ and $( A \to B )$ is the implication $( A \Rightarrow B )$ . In categorical terms, the simply typed λ-calculus corresponds to cartesian closed categories in the evident way.

The principal innovation of Martin-Löf’s dependent type theory over the simply typed λ-calculus is that types are allowed to depend on or “vary over” other types, thereby yielding a more complex and expressive theory. The meaning of type dependence is that, when A is a given type, it is possible for a family $( B _ { x } ) _ { x : A }$ of types to occur indexed by A. The theory also allows families of types which are themselves indexed by families of types, and so forth. The basic operations of the theory then correspond to indexed sums and products. These operations, together with type dependence, allow us to regard dependent type theory as an extension of the Curry-Howard correspondence to first-order (intuitionistic) logic. Similarly, the kinds of categories corresponding to dependent type theory are locally cartesian closed categories.

We now present the syntax of Martin-Löf type theory in more detail together with an interpretation, due to Seely [17], in locally cartesian closed categories. This interpretation is “non-split” in the sense that it does not model substitution on the nose, but only up to canonical natural isomorphism, due to the pseudo-functoriality introduced by a choice of pullbacks (cf. [5] and [7]). Because we are mostly interested in type theory as an internal language for categories this conflation of isomorphic objects will not concern us here. The homotopy theoretical interpretation will be given in Section 3.

2.1. Forms of judgement. The syntax of type theory is given by first indicating four “forms of judgement”. These are the basic kinds of statement which can be formally made in the theory. The first form of judgement is the type declaration ⊢ A : type which says that A is a type. In a fixed locally cartesian closed category C such a judgement is interpreted as an object A of C. As mentioned above, when A is a type it is possible to consider A-indexed families of types. That $B ( x )$ is an A-indexed family of types is indicated by the following form of judgement

$$
x: A \vdash B (x): \text { type }.\tag{1}
$$

Such a judgment is interpreted as an arrow $f : B { \longrightarrow } A$ with codomain A following the usual categorical treatment of indexed families.

In (1) the part $x : A$ to the left of the turnstile ⊢ is called the context of the judgement. More generally, a list of variable declarations

$$
x _ {0}: A _ {0}, x _ {1}: A _ {1}, \ldots , x _ {n}: A _ {n}
$$

is a context whenever the judgements $\vdash A_0 : \mathrm{type}$ and

$$
x _ {0}: A _ {0}, \ldots , x _ {m}: A _ {m} \vdash A _ {m + 1}: \mathrm{type}
$$

are derivable for $0 \leq m < n$ . Upper-case Greek letters $\Gamma, \Delta, \ldots$ are reserved as names for contexts. Contexts are interpreted in the natural way as chains

$$
A _ {n} \longrightarrow A _ {n - 1} \longrightarrow \dots \longrightarrow A _ {0}\tag{2}
$$

of arrows. The empty context is interpreted as the terminal object.

In addition to judgements of the form $\Gamma \vdash A : \mathrm{type}$ there are also judgements of the form

$$
\Gamma \vdash a: A,\tag{3}
$$

which state that a is a term of type A in the context Γ. In the empty context a term $a : A$ is interpreted as a global section $1 \longrightarrow A$ of the object A. Similarly, when Γ is interpreted as a chain of arrows of the form (2) the judgement (3) is interpreted as a section $a : A _ { n } { \longrightarrow } A$ of the interpretation $A \longrightarrow A _ { n }$ of $\Gamma \vdash A : \mathrm{type}$.

Finally, there are also forms of judgement governing definitional equality of types and terms as follows:

$$
\begin{array}{l} \Gamma \vdash A = B: \text {type}, \\ \Gamma \vdash a = b: A, \end{array}
$$

which are interpreted as identities in C. Henceforth, when no confusion will result, explicit mention of contexts will be elided.

2.2. Dependent sums and products. Given an A-indexed family of types $B ( x )$ the dependent sum $\Sigma _ { x : A } . B ( x )$ and the dependent product $\Pi _ { x : A } . B ( x )$ can be formed. This is usually stated as the following formation rules

$$
\frac {x : A \vdash B (x)}{\vdash \Sigma_ {x : A} . B (x) : \mathrm{type}} \Sigma \text {form.} \qquad \text {and} \qquad \frac {x : A \vdash B (x)}{\vdash \Pi_ {x : A} . B (x) : \mathrm{type}} \Pi \text {form.}
$$

Under the Curry-Howard correspondence, dependent sums correspond to existential quantifiers and dependent products correspond to universal quantifiers. The behavior of these types is specified by introduction, elimination and conversion rules, which can be thought of either in terms of manipulation of indexed families or their logical significance. For example, the introduction rule for $\Pi _ { x : A } . B ( x )$ is stated as

$$
\frac {x : A \vdash f (x) : B (x)}{\vdash \lambda_ {x : A} . f (x) : \Pi_ {x : A} . B (x)} \Pi \text {   intro.   }
$$

which states that if $f$ is a family of terms $f ( x ) : B ( x )$ , then there is a term $\lambda _ { x : A } . f ( x )$ of type $\Pi _ { x : A } . B ( x )$ . Similarly, the elimination rule

$$
\frac {\vdash g : \Pi_ {x : A} . B (x) \quad \vdash a : A}{\vdash \operatorname{app} (g , a) : B (a)} \Pi \text { elim. }
$$

corresponds to the application of an element $g$ of the indexed product to $a : A$. Finally, the following conversion rule for dependent products states that the application term $\operatorname{app} ( g , a )$ behaves correctly when $g$ is itself of the form $\lambda _ { x : A } . f ( x )$ :

$$
\frac {x : A \vdash f (x) : B (x) \quad \vdash a : A}{\vdash \operatorname{app} \bigl (\lambda_ {x : A} . f (x) , a \bigr) = f (a) : B (a)}   \Pi   \text {conv.}
$$

The dependent sums $\Sigma _ { x : A } . B ( x )$ are likewise required to obey suitable introduction, elimination and conversion rules. When types A and B do not depend on any variables, the usual product type $( A \times B )$ and exponential type $( A \to B )$ from the simply typed λ-calculus are recovered as $\Sigma_{x:A}.B$ and $\Pi _ { x : A } . B$ , respectively.

In a locally cartesian closed category C, the dependent products and sums are interpreted in the natural way using, respectively, the right and left adjoints to the pullback functors.

2.3. Identity types. In addition to dependent sums and products it is required that for each type A and terms $a , b : A$ , there exists a type $\operatorname{Id}_A ( a , b )$ called the identity type which provides the only explicit form of type dependence in the theory considered here. I.e., unlike dependent products and sums, the formation rule for the identity type introduces new type dependencies:

$$
\frac {\vdash a : A \qquad \vdash b : A}{\vdash \operatorname{Id} _ {A} (a , b) : \text {type}} \text {Id form.}\tag{4}
$$

Under the Curry-Howard correspondence, this type is regarded as the proposition which states that a and b denote identical proofs of the proposition A. The introduction rule

$$
\frac {\vdash a : A}{\vdash r _ {A} (a) : \operatorname{Id} _ {A} (a , a)} \text {   Id   intro.   }\tag{5}
$$

states that given a term $a : A$ there is always a witness $r _ { A } ( a )$ to the proposition that a is identical to itself. We call $r _ { A } ( a )$ the reflexivity term. On the other hand, the distinctive elimination rule

$$
\begin{array}{c} x: A, y: A, z: \operatorname{Id} _ {A} (x, y) \vdash D (x, y, z): \text {type} \\ \vdash p: \operatorname{Id} _ {A} (a, b) \qquad x: A \vdash d (x): D \bigl (x, x, r _ {A} (x) \bigr) \\ \hline \vdash J _ {A, D} (d, a, b, p): D (a, b, p) \end{array} \text {Id elim.}\tag{6}
$$

can be recognized as a form of Leibniz’s law. Finally, the conversion rule

$$
\begin{array}{c} x: A, y: A, z: \operatorname{Id} _ {A} (x, y) \vdash D (x, y, z): \text {type} \\ \vdash a: A \qquad x: A \vdash d (x): D \bigl (x, x, r _ {A} (x) \bigr) \\ \hline \vdash J _ {A, D} (d, a, a, r _ {A} (a)) = d (a): D (a, a, r _ {A} (a)) \end{array} \text {Id conv.}\tag{7}
$$

indicates that the elimination term is equal to d(a) when p is the reflexivity term.

2.4. Locally cartesian closed categories are extensional. A model of Martin-Löf type theory is extensional if the following reflection rule is satisfied:

$$
\frac {\vdash p : \operatorname{Id} _ {A} (a , b)}{\vdash a = b : A .} \text {   Id   refl.   }\tag{8}
$$

I.e., the identity type $\operatorname{Id} _ { A } ( a , b )$ captures no more information than whether or not a and b are definitionally equal. Although type checking is decidable in the intensional theory, it fails to be in the extensional theory obtained by adding (8) as a rule governing identity types. This fact is the principal motivation for studying intensional rather than extensional type theories (cf. [18] for a more thorough discussion of the phenomenon of intensionality and the difference between intensional and extensional forms of the theory). Under the general interpretation in locally cartesian closed categories sketched above the reflection rule is always valid.

Proposition 2.1. In the standard interpretation given above, every locally cartesian closed category $\mathcal { C }$ is extensional.

Proof. Note that it suffices to consider “parameterized” versions of the rules governing identity types. I.e., the rules given above are equivalent, by the structural rules of the theory, to the rules obtained by replacing any terms $a , b : A$ and $p : \operatorname{Id} _ { A } ( a , b )$ by variables $x , y : A$ and $z : \operatorname{Id} _ { A } ( x , y )$ , and stating judgements in the appropriate context. E.g., (6) is equivalent to

$$
\begin{array}{c} x: A, y: A, z: \operatorname{Id} _ {A} (x, y) \vdash D (x, y, z): \text {type} \\ x: A \vdash d (x): D \bigl (x, x, r _ {A} (x) \bigr) \\ \hline x, y: A, z: \operatorname{Id} _ {A} (x, y) \vdash J _ {A, D} (d, x, y, z): D (x, y, z). \end{array}
$$

As such, it suffices to prove that, when A is an object of ${ \mathcal { C } } ,$ any object $\operatorname{Id} _ { A }$ satisfying the introduction, elimination and conversion rules for the identity type is isomorphic to the diagonal $\Delta : A { \longrightarrow } A \times A$ . By the formation and introduction rules (4) and (5), there exists a factorization

(9)

![Diagram (9): factorization of the diagonal through the identity object](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/5b2e56951e2b90ef5c5c328671fb7a3c04b30fbaa8b32c944f5dd9d2ba8dea71.jpg)


of the diagonal. In the interpretation, $r$ may itself be regarded as a type over $\operatorname{Id}_A$. By (9), this type satisfies the hypotheses of the elimination rule and therefore there exists a section $J : \operatorname{Id}_A \longrightarrow A$ of $r$,

![Diagram showing the section J of r](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/460a861191bdf5c61a5fd71a9061a0e43ce33c1a24afadefec524ed2acc35a21.jpg)


as required.

We now consider homotopy models of type theory, which do not validate the reflection rule.

## 3. Homotopy Theoretic Models

In order to obtain models of type theory which do not validate the reflection rule additional higher-dimensional structure must be considered in the interpretation. One way to add such structure is via the device of weak-factorization systems and Quillen model categories (cf. [16] and [3]).

3.1. Weak factorization systems. In any category ${ \mathcal { C } } ,$ given maps $f : A \longrightarrow B$ and $g : C \longrightarrow D$ , we write

$$
f \pitchfork g
$$

to indicate that $f$ has the *left-lifting property* (LLP) with respect to $g$. I.e., for any commutative square

$$
\begin{array}{c} A \xrightarrow {h} C \\ f \Biggl \downarrow \\ B \xrightarrow {k} D \end{array} \Biggl \downarrow g
$$

there exists a map $l : B \longrightarrow C$ such that $g \circ l = k$ and $l \circ f = h$. Similarly, if $\mathfrak{M}$ is any collection of maps, we denote by ${}^{\pitchfork}\mathfrak{M}$ the collection of maps in $\mathcal{C}$ having the LLP with respect to all maps in $\mathfrak{M}$. The collection of maps $\mathfrak{M}^{\pitchfork}$ is defined similarly.

A weak factorization system $(\mathfrak{L}, \mathfrak{R})$ in a category $\mathcal{C}$ consists of two collections $\mathfrak{L}$ (the *left class*) and $\mathfrak{R}$ (the *right class*) of maps in $\mathcal{C}$ such that

(1) Every map $f : A { \longrightarrow } B$ has a factorization as

![Weak factorization of a map f as p composed with i](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/6b34dd16b2f035fd3c34f68d875fe873fa6636dbb3c50b6bc169b77618b37855.jpg)


where $i$ is a member of $\mathfrak{L}$ and $p$ is a member of $\mathfrak{R}$.

$$
(2) \mathfrak {L} ^ {\pitchfork} = \mathfrak {R} \text {   and   } \mathfrak {L} = ^ {\pitchfork} \mathfrak {R}.
$$

3.2. Model categories. A (closed) model category [16] is a bicomplete category $\mathcal{C}$ equipped with subcategories $\mathfrak{F}$ (fibrations), $\mathfrak{C}$ (cofibrations) and $\mathfrak{W}$ (weak equivalences) satisfying the following two conditions:

(1) (“Three-for-two”) Given a commutative triangle

![Commutative triangle for the three-for-two property](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/39bf4ed74e3c591519abbfca492eacd5c6e58790d45c6d2a25c18588619f5058.jpg)


if any two of $f , g , h$ are weak equivalences, then so is the third.

(2) Both $(\mathfrak{C}, \mathfrak{F} \cap \mathfrak{W})$ and $(\mathfrak{C} \cap \mathfrak{W}, \mathfrak{F})$ are weak factorization systems.

A map f is an acyclic cofibration if it is in $\mathfrak { C } \cap \mathfrak { W }$ , i.e. both a cofibration and a weak equivalence. Similarly, an acyclic fibration is a map in ${ \mathfrak { F } } \cap { \mathfrak { W } }$ , i.e. which is simultaneously a fibration and a weak equivalence. An object A is said to be fibrant if the canonical map $A \longrightarrow 1$ is a fibration. Similarly, A is cofibrant if $0 \longrightarrow A$ is a cofibration.

Examples of model categories include the following:

(1) The category Top of topological spaces with fibrations the Serre fibrations, weak equivalences the weak homotopy equivalences and cofibrations those maps which have the LLP with respect to acyclic fibrations. The cofibrant objects in this model structure are retracts of spaces constructed, like CW complexes, by attaching cells.

(2) The category SSet of simplicial sets with cofibrations the monomorphisms, fibrations the Kan fibrations and weak equivalences the weak homotopy equivalences. The fibrant objects for this model structure are the Kan complexes.

(3) The category Gpd of (small) groupoids with cofibrations the functors injective on objects, fibrations the Grothendieck fibrations and weak equivalences the categorical equivalences. Here all objects are both fibrant and cofibrant.

The reader should consult, e.g., [9] or [6] for further examples and details.

3.3. Path objects. Recall from [9], that in a model category C a (very good) path object $A ^ { I }$ for an object A consists of a factorization

![Path-object factorization of the diagonal of A](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/bf9451d2e342205e16e91282fe4cd2703e8b02523881cb570b6b18cfc685c926.jpg)


of the diagonal map $\Delta : A { \longrightarrow } A \times A$ as an acyclic cofibration r followed by a fibration p. Paradigm examples of path objects are given by exponentiation by the “unit interval” I in either Gpd or, when the object A is a Kan complex, in SSet. In Gpd, I is the connected groupoid with exactly two objects (i.e., the “arrow category”) and in SSet it is the 1-simplex $\Delta[1]$.

Path objects may also be fruitfully considered in the context of weak factorization systems, where the left class L is thought of as the acyclic cofibrations and the right class R as the fibrations. In both weak factorization systems and model categories path objects are guaranteed to exist, but need not be uniquely determined. Moreover, the path object construction is often functorial.

3.4. The interpretation. Whereas the idea of the Curry-Howard correspondence is often summarized by the slogan “Propositions as Types”, the idea underlying the interpretation of type theory in weak factorization systems and model categories is

**Fibrations as Types.**

Specifically, assume that C is a finitely complete category with a weak factorization system (L, R). Because most interesting examples arise from model categories, we refer to maps in $\mathfrak { L }$ as acyclic cofibrations and those in $\mathfrak{R}$ as fibrations. We describe the interpretation in the style of an “internal language” for ${ \mathcal { C } } ,$ as in Section 2 for locally cartesian closed categories.

In such a category $\mathcal{C}$, a judgement $\vdash A : \mathrm{type}$ is interpreted as a fibrant object $A$ of $\mathcal{C}$. Similarly, $x : A \vdash B(x) : \mathrm{type}$ is interpreted as a fibration $f : B \longrightarrow A$. Contexts are interpreted as chains of fibrations. Terms $\Gamma \vdash a : A$ in context are interpreted, as usual, as sections of the interpretation of $\Gamma \vdash A : \mathrm{type}$.

Thinking, in this way, of fibrant objects as types and fibrations as dependent types, the natural interpretation of the identity type $\operatorname{Id}_A(a,b)$ should be as the “fibrant object” of paths in $A$ from $a$ to $b$, and $x,y : A \vdash \operatorname{Id}_A(x,y) : \mathrm{type}$ should be “the” fibrant object of all paths in $A$. That is, it should be a path object for $A$.

We now show that this interpretation soundly models a form of type theory with identity types (see Appendix A for the details of this theory). The interpretation of type formers other than identity types, together with some of the coherence issues related to the interpretation, is discussed in Section 4.

Theorem 3.1. Let C be a finitely complete category with a weak factorization system and a functorial choice $( - ) ^ { I }$ of path objects in ${ \mathcal { C } } ,$ and all of its slices, which is stable under substitution. I.e., given any fibration $B { \longrightarrow } A$ and $\sigma : A ^ { \prime } { \longrightarrow } A$

$$
\sigma^ {*} (B ^ {I}) \cong (\sigma^ {*} B) ^ {I}.
$$

Then $\mathcal { C }$ is a model of a form of Martin-Löf type theory with identity types.

Proof. We may work in the empty context since the relevant structure is stable under slicing. Given such a choice of path objects, we interpret, for a fibrant object $A$, the judgement $x,y : A \vdash \operatorname{Id}_A(x,y) : \mathrm{type}$ as the path-object fibration $p : A^I \longrightarrow A \times A$. Because $p$ is a fibration, the formation rule (4) is satisfied. Similarly, the introduction rule (5) is valid because $r : A \longrightarrow A^I$ lies over the diagonal.

For the elimination and conversion rules, assume that the following premisses are given

$$
\begin{array}{c} x: A, y: A, z: \operatorname{Id} _ {A} (x, y) \vdash D: \text {type}, \\ x: A \vdash d (x): D (x, x, r _ {A} (x)). \end{array}
$$

As such, there exists a fibration $g : D { \longrightarrow } A ^ { I }$ together with a map d : $A \longrightarrow D$ such that $g \circ d = r$ . This data yields the following commutative square:

![Lifting square for the identity-type elimination rule](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/3c75c8ee70320072cb5e232bd4b23cf7dd094ea56aa926a29622a797e2d54aa8.jpg)


Because $g$ is a fibration and r is, by definition, an acyclic cofibration, there exists a diagonal filler.

(10)

![Diagram (10): diagonal filler J](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/42ad802239a84ff0745f1924dcf589f9ff0bfb5363a0227ccb048e2e0ca25458.jpg)


Choose such a filler J as the interpretation of the term:

$$
x, y: A, z: \operatorname{Id} _ {A} (x, y) \vdash J _ {A, D} (d, x, y, z): D (x, y, z).
$$

Commutativity of the bottom triangle of (10) is precisely the conclusion of the elimination rule (6) and commutativity of the top triangle is the conversion rule (7). □

Examples of categories satisfying the hypotheses of Theorem 3.1 include Gpd, SSet and many simplicial model categories [16] (including, e.g., simplicial sheaves and presheaves). We include a proof of this fact for the benefit of those readers who are familiar with simplicial model categories. This example will be considered in more detail in [19].

Corollary 3.2. Every simplicial model category $\mathcal{C}$ in which $\mathfrak{C}$ is the class of monomorphisms satisfies the hypotheses of Theorem 3.1, and is therefore a model of intensional type theory.

Proof. Let I be the unit interval $\Delta [ 1 ]$ in SSet, and consider, for any fibrant object $A$ of $\mathcal{C}$ , the factorization of the diagonal given by

![Simplicial path-object factorization using A to the power I](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/56af1cc1-c350-476f-b474-53b417d36e50/cbd27c72b6d7ca5ca9ee0ac22da9489b8414f01c2dfa6ad70d51bae5ceb94958.jpg)


where r is the “constant loop” map obtained as the transpose, under the (enriched) adjunctions involved, of the map $I { \longrightarrow } { \mathcal { C } } [ A , A ]$ obtained by composing the canonical map $I \longrightarrow 1$ with the insertion of identities map $1 \longrightarrow \mathcal { C } [ A , A ]$ and $p$ is the map obtained by $A ^ { I } { \longrightarrow } A ^ { \partial I }$ induced by the inclusion of the boundary ∂I into I. Because $\partial I { \longrightarrow } I$ is a monomorphism and $A$ is fibrant it follows that $p$ is a fibration. Because r is a simplicial homotopy equivalence it is also a weak equivalence. The required pullback stability is seen to hold using the adjunctions defining the factorization. Stability under slicing of this choice of factorization (as well as the structure defining simplicial model categories) is a routine verification. □

## 4. Additional Topics

We now briefly consider the particular features of the type theory occurring as the internal language of model categories, as well as the connection of this work with the groupoid model of Hofmann and Streicher [8]. These topics will be addressed fully in [19].

4.1. The internal language of model categories. The form of type theory to which Theorem 3.1 applies differs from the standard theory presented in, say, [13] in two ways. Namely, because arbitrary model categories need not be locally cartesian closed — or, even if they are, need not have Π functors which preserve fibrations — such a category may not possess sufficient structure to interpret dependent products in the standard way. However, for the purposes of modelling type theory this is not much of a limitation since most model categories do possess well behaved Π functors. So, for example, SSet as well as most other presheaf model categories do, qua toposes with appropriate model structures, support the interpretation of dependent products. Note that the rules for dependent sums are, trivially, always valid in this interpretation because fibrations are stable under composition. The second distinguishing feature of the internal language of model categories is that the interpretation of J terms need not satisfy the “Beck-Chevalley” condition — traditionally assumed as part of Martin-Löf type theory — which states that, given $v : A \ \vdash \ B ( v )$ : type and $c : A$ together with the other hypotheses of the elimination rule,

$$
\left(J _ {B (v), D} \bigl (d (v), a (v), b (v), p (v) \bigr)\right) [ c / v ] = J _ {B (c), D} \bigl (d (c), a (c), b (c), p (c) \bigr).\tag{11}
$$

The reason that (11) need not hold is that in interpreting the J term a choice of lift (10) is made, and it may not, in general, be possible to choose such lifts in a way which is compatible with pullback. Nonetheless, there will always exist a (right) homotopy between the interpretations of these terms and, in particular,

$$
\operatorname{Id} \left(J _ {B (v), D} (d (v), a (v), b (v), p (v)) [ c / v ], J _ {B (c), D} (d (c), a (c), b (c), p (c))\right)
$$

is always inhabited. As such, the theory must be formulated either as it is here, without requiring (11), or as a form of dependent type theory with explicit substitution [1, 5].

However, we believe that the failure of (11) to hold constitutes a virtue, rather than a defect, of homotopy-theoretic models. Indeed, from the perspective of homotopy theory, higher-dimensional category theory, and, indeed, mechanical implementation of type theory, an internal language with some (limited) form of explicit substitution is quite acceptable. The detailed syntax of this theory will be described in [19].

4.2. Models satisfying the coherence condition. Although the form of type theory modelled in all model categories and finitely complete categories with weak factorization systems is interesting in its own right, it is natural to consider models satisfying the coherence condition (11). A detailed analysis of models satisfying (11) will be found in [19]; for now, we sketch one way to obtain such models. In order to simplify the discussion we assume the ambient category C is a cartesian closed model category (or an appropriately enriched model category). Then, if C contains a unit interval I satisfying certain basic axioms such that exponentiation $A ^ { I }$ yields a path object for each A, it is possible to define a (fibered) endofunctor $T : { \mathcal { C } } \longrightarrow { \mathcal { C } }$ the pointed algebras of which are distinguished fibrations called split fibrations (and in many cases T will be a monad, although this is not strictly necessary). Instead of interpreting types as fibrations we now interpret types as split fibrations in this sense. Assuming that I possesses appropriate structure it is possible to choose lifts (10) which satisfy (11). For example, the Hofmann-Streicher model in Gpd is obtained in this way from the model structure. It remains an open question whether it is possible to prove a precise coherence (or strictification) theorem, relating homotopy-theoretic models which do not satisfy (11) with models which do, analogous to the result of Hofmann [7] which, in a sense, solves the coherence issue related to the interpretation extensional type theory in locally cartesian closed categories.

4.3. Acknowledgements. We would like to thank Andrej Bauer, Nicola Gambino, André Joyal, Per Martin-Löf and Alex Simpson for discussions of this material. We also thank Erik Palmgren and Richard Garner for inviting us to speak at the workshop “Identity Types - Topological and Categorical Structure” held at Uppsala in November of 2006. Finally, we give special thanks to Ieke Moerdijk for suggesting this research topic and to Thomas Streicher for many useful discussions.

## Appendix A. The Syntax of Type Theory

The form of type theory validated as indicated in Theorem 3.1 consists of (4)- (7) together with the usual structural rules (cf. [13, 15]) and the following “Beck-Chevalley” rules for the identity type and reflexivity terms:

$$
\begin{array}{c} \frac {x : C \vdash A (x) : \text {type} \quad x : C \vdash a (x) , b (x) : A (x) \quad \vdash c : C}{\vdash \left(\operatorname{Id} _ {A (x)} \bigl (a (x) , b (x) \bigr)\right) [ c / x ] = \operatorname{Id} _ {A (c)} \bigl (a (c) , b (c) \bigr) : \mathrm{type}} \text {Id B.-C}. \\ \frac {x : C \vdash A (x) : \text {type} \quad x : C \vdash a (x) : A (x) \quad \vdash c : C}{\vdash \left(r _ {A (x)} \bigl (a (x) \bigr)\right) [ c / x ] = r _ {A (c)} \bigl (a (c) \bigr) : \operatorname{Id} _ {A (c)} (a (c) , a (c))}   r   \text {B.-C}. \end{array}
$$

## References



[1] M. Abadi, L. Cardelli, P.-L. Curien, and J.-J. Lévy. Explicit substitutions. In Proceedings of the 17th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, pages 31–46, New York, 1989. ACM Press.





[2] Y. Bertot and P. Castéran. Interactive Theorem Proving and Program Development. Springer, Berlin-Heidelberg, 2004.





[3] A. K. Bousfield. Constructions of factorization systems in categories. Journal of Pure and Applied Algebra, 9:207–220, 1977.





[4] C. Coquand and T. Coquand. Structured type theory. In Proceedings of the Workshop on Logical Frameworks and Meta-Languages (LFM’99), Paris, 1999.





[5] P.-L. Curien. Substitution up to isomorphism. Fundamenta Informaticae, 19:51–86, 1993.





[6] W. G. Dwyer and J. Spalinski. Homotopy theories and model categories. In I. M. James, editor, Handbook of Algebraic Topology, pages 73–126. North-Holland, Amsterdam, 1995.





[7] M. Hofmann. On the interpretation of type theory in locally cartesian closed categories. In J. Tiuryn and Leszek Pacholski, editors, Computer Science Logic 1994, pages 427–441. Springer, 1995.





[8] M. Hofmann and T. Streicher. The groupoid interpretation of type theory. In G. Sambin and J. Smith, editors, Twenty-Five Years of Constructive Type Theory, volume 36 of Oxford Logic Guides, pages 83–111. Oxford University Press, Oxford, 1998.





[9] M. Hovey. Model Categories, volume 63 of Mathematical Surveys and Monographs. American Mathematical Society, Providence, Rhode Island, 1999.





[10] A. Joyal. Quasi-categories and Kan complexes. Journal of Pure and Applied Algebra, 175:207–222, 2002.

[11] A. Joyal. Notes on quasi-categories. Unpublished manuscript, 2007.

[12] J. Lurie. Higher topos theory. Unpublished manuscript, available on the arXiv as arXiv:math/0608040, 2007.

[13] P. Martin-Löf. An intuitionistic theory of types: predicative part. In H. E. Rose and J. C. Shepherdson, editors, *Logic Colloquium ’73*, pages 73–118. North-Holland, 1975.

[14] F. Morel and V. Voevodsky. $\mathbb{A}^1$-homotopy theory of schemes. *Institut des Hautes Études Scientifiques. Publications Mathématiques*, 90:45–143, 1999.

[15] B. Nordström, K. Petersson, and J. M. Smith. *Programming in Martin-Löf’s Type Theory: An Introduction*. Oxford University Press, 1990.

[16] D. Quillen. *Homotopical Algebra*. Lecture Notes in Mathematics. Springer-Verlag, 1967.

[17] R. A. G. Seely. Locally cartesian closed categories and type theory. *Mathematical Proceedings of the Cambridge Philosophical Society*, 95:33–48, 1984.

[18] T. Streicher. *Investigations into Intensional Type Theory*. Habilitationsschrift, Ludwig-Maximilians-Universität München, 1993.

[19] M. A. Warren. *Homotopy Theoretic Aspects of Constructive Type Theory*. Ph.D. thesis, Carnegie Mellon University. In preparation.
