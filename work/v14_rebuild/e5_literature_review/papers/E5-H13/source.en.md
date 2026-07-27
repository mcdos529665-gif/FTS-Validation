# The identity type weak factorisation system

Nicola Gambino <sup>a,b,∗</sup>, Richard Garner <sup>c</sup> 

<sup>a</sup> Department of Computer Science, University of Leicester, University Road, LE1 7RH, England, UK 

<sup>b</sup> Centre de Recerca Matemàtica, Apartat 50, E-08193 Bellaterra, Spain 

<sup>c</sup> Department of Mathematics, Uppsala University, Box 480, S-751 06, Uppsala, Sweden 

## a r t i c l e i n f o

Article history: Received 30 March 2008 Received in revised form 24 July 2008 Accepted 15 August 2008 Communicated by P.-L. Curien 

Keywords: Dependent type theory Identity type Weak factorisation system 

## a b s t r a c t

We show that the classifying category C(<sup>T</sup>) of a dependent type theory <sup>T</sup> with axioms for identity types admits a non-trivial weak factorisation system. We provide an explicit characterisation of the elements of both the left class and the right class of the weak factorisation system. This characterisation is applied to relate identity types and the homotopy theory of groupoids. 

© 2008 Elsevier B.V. All rights reserved. 

## 1. Introduction

From the point of view of mathematical logic and theoretical computer science, Martin-Löf’s axioms for identity types [25] admit a conceptually clear explanation in terms of the propositions-as-types correspondence [14 22 28] The fundamenta idea behind this explanation is that, for any two elements a, b of a type A, we have a new type ${ \mathrm { I d } } _ { A } ( a , b )$ , whose elements are to be thought of as proofs that a and b are equal. Yet, identity types determine a highly complex structure on each type, which is far from being fully understood. A glimpse of this structure reveals itself as soon as we start applying the construction of identity types iteratively: not only do we have proofs of equality between two elements of a type, but also of proofs of equality between such proofs, and so on. The difficulty of isolating the structure determined by identity types is closely related to the problem of describing a satisfactory category-theoretic semantics for them. For example, the semantics arising from locally cartesian closed categories [9,30] validates not only the axioms for identity types, but also additional axioms, known as the reflection rules, which make identity types essentially trivial. To improve on this unsatisfactory situation and obtain models that do not validate the reflection rules, Awodey and Warren have recently introduced a semantics of identity types in categories equipped with a weak factorisation system [2]. 

Our aim here is to advance our understanding of the categorical structure implicit in the axioms for identity types. We do so by providing further evidence of a close connection between the axioms for identity types and the notion of a weak factorisation system. Our main result states that if <sup>T</sup> is a dependent type theory with the axioms for identity types, then its classifying category C(<sup>T</sup>) admits a non-trivial weak factorisation system, which we shall refer to as the identity type weak factorisation system. This result should be regarded as analogous to the fundamental result exhibiting the structure of a cartesian closed category on the classifying category of the simply-typed λ-calculus [19,29]. As such, it provides also a contribution to the development of a functorial semantics [20] for dependent type theories [2,5,7,10,15,21]. 

A remarkable feature of the identity type weak factorisation system is that its definition does not involve the notion of identity types, but only a canonical class of maps in C(<sup>T</sup>), generally referred to as display maps [15,33]. Indeed, the axioms for identity types are used only to verify that the appropriate axioms hold. After having established the existence of the identity type weak factorisation system, we will provide an explicit characterisation of its classes of maps. This will lead us to two applications. The first establishes a stability property of the identity type weak factorisation system; the second provides further insight into the relationship between dependent type theories with identity types and the category of groupoids, which we denote Gpd. 

The idea of relating identity types and groupoids dates back to the discovery of the groupoid model of type theory by Hofmann and Streicher [12], who showed that the axioms for identity types allow us to construct a groupoid out of every type. We develop this idea in three directions. First, we generalise it by constructing a groupoid out of every context, which we think of as a family of types, rather than out of a single type. Secondly, we extend this construction to a functor $\mathcal { F } : \mathcal { C } ( \mathbb { T } ) $ Gpd. Finally, we use the functor F to relate the identity type weak factorisation system to the natural Quillen model structure on the category of groupoids [1,17], by showing that the identity type weak factorisation system is mapped into the weak factorisation system determined by injective equivalences and Grothendieck fibrations in Gpd. 

## 2. Identity types

The dependent type theories that we consider allow us to make judgements of four forms: 

$$
A \in \text { Type }, \quad a \in A, \quad A = B \in \text { Type }, \quad a = b \in A.\tag{1}
$$

They assert, respectively, that A is a type, that a is an element of A, that A and B are definitionally equal types, and that a and b are definitionally equal elements of A. We speak of definitional equality, rather than just equality, since the axioms for identity types will provide us with a second notion of equality, which we will refer to as propositional equality. The distinction between definitional and propositional equality plays a fundamental role for our purposes. As usual, the judgements in (1) may also be made relative to contexts, which consist of lists of variable declarations of the form 

$$
\varPhi = \left(x _ {0} \in A _ {0}, x _ {1} \in A _ {1} (x _ {0}), \dots , x _ {n} \in A _ {n} (x _ {0}, \dots , x _ {n - 1})\right).\tag{2}
$$

For the context in (2) to be well-formed, it is necessary that the variables $x _ { 0 } , \ldots , x _ { n }$ are distinct, and that the following sequence of judgements is derivable 

$$
\begin{array}{l} A _ {0} \in \text { Type }, \\ (x _ {0} \in A _ {0})   A _ {1} (x _ {0}) \in \text { Type }, \\ \dots \\ (x _ {0} \in A _ {0},   \ldots ,   x _ {n - 1} \in A _ {n - 1} (x _ {0},   \ldots ,   x _ {n - 2}))   A _ {n} (x _ {0},   \ldots ,   x _ {n - 1}) \in \text { Type }. \end{array}
$$

Whenever we mention contexts, we implicitly assume that they are well-formed. We write (Φ) J to express that a judgement $\mathcal { J }$ holds under the assumptions in Φ. The axioms for a dependent type theory will be stated here as deduction rules of the form 

$$
\frac {(\Phi_ {1})   \mathcal {J} _ {1} \quad \cdots \quad (\Phi_ {n})   \mathcal {J} _ {n}}{(\Phi)   \mathcal {J}}.
$$

From now on, we work with a fixed dependent type theory <sup>T</sup>. The only assumption that we make on <sup>T</sup> is that it contains the basic axioms stated in Appendix. For more information on dependent type theories, see [22,24]. 

We briefly recall the definition of the classifying category C(<sup>T</sup>) associated to <sup>T</sup>. For a context Φ as in (2) and a context $\psi = ( y _ { 0 } \in B _ { 0 } , \ldots , y _ { m } \in B _ { m } ( y _ { 0 } , \ldots , y _ { m - 1 } ) ) $ , a context morphism $f : \phi  \psi$ consists of a sequence $f = ( b _ { 0 } , \ldots , b _ { m } )$ such that the following judgements are derivable 

$$
\begin{array}{l} (\varPhi)   b _ {0} \in B _ {0}, \\ (\varPhi)   b _ {1} \in B _ {1} (b _ {0}), \\ \dots \\ (\varPhi)   b _ {m} \in B _ {m} (b _ {0}, \ldots , b _ {m - 1}). \end{array}
$$

We can define an equivalence relation on contexts by considering two contexts to be equivalent if they coincide up to renaming of their free variables and up to componentwise definitional equality. Similarly, we can define an equivalence relation on context morphisms by considering two context morphisms from Φ to Ψ to be equivalent if they coincide up to renaming of the free variables in Φ and up to pointwise definitional equality. The classifying category C(<sup>T</sup>) can then be defined as having equivalence classes of contexts as objects, and equivalence classes of context morphisms as maps. Composition is defined via substitution, while identity maps are defined in the evident way [26]. When working with C(<sup>T</sup>), we implicitly identify contexts and context morphisms up to the equivalence relations defined above, without introducing additional notation. The empty context, written ( ) here, is a terminal object in C(<sup>T</sup>). In what follows, we will be particularly interested in the class of context morphisms known as as display maps [15,33]. These are context morphisms of the form $( { \cal { T } } , x \in A )  { \cal { T } }$ , defined by projecting away the variable $x \in A ,$ where Γ is a context and A is a type relative to Γ . As we will see in Section 4, display maps play a crucial role in the definition of the identity type weak factorisation system 

To work with the category C(<sup>T</sup>) and its slices, it will be convenient to use some of the abbreviations for manipulating contexts developed in [6]. Let us consider a fixed context Γ . For a sequence of variable declarations as in (2), we write $( T ) \phi \in \operatorname { C x t }$ to abbreviate the following sequence of judgements 

$$
\begin{array}{l} (\Gamma)   A _ {0} \in \text { Type }, \\ (\Gamma , x _ {0} \in A _ {0})   A _ {1} (x _ {0}) \in \text { Type }, \\ \dots \\ (\Gamma , x _ {0} \in A _ {0}, \ldots , x _ {n - 1} \in A _ {n - 1} (x _ {0}, \ldots , x _ {n - 1}))   A _ {n} (x _ {0}, \ldots , x _ {n - 1}) \in \text { Type }. \end{array}
$$

When these are derivable, we say that Φ is a dependent context relative to Γ . Dependent contexts relative to the empty context are simply contexts. If we have a dependent context Φ relative to $T ,$ , we obtain a new context $( T , \phi )$ by concatenation, and an evident map $( \boldsymbol { { \Gamma } } , \boldsymbol { \phi } )  \boldsymbol { { \Gamma } }$ , projecting away the variables in Φ. Maps of this form will be referred to as dependent projections. Note that the class of dependent projections can be seen as the closure under composition of the class of display maps. For a context Φ relative to $T ,$ , as above, and a sequence $a = ( a _ { 0 } , a _ { 1 } , \ldots , a _ { n } )$ , we write $( T ) a \in \phi$ to abbreviate the following sequence of judgements 

$$
\begin{array}{l} (\Gamma) a _ {0} \in A _ {0}, \\ (\Gamma) a _ {1} \in A _ {1} (a _ {0}), \\ \dots \\ (\Gamma) a _ {n} \in A _ {n} (a _ {0}, \ldots , a _ {n - 1}). \end{array}
$$

When these can be derived, we say that a is a dependent element of Φ relative to Γ . Dependent elements of this form are the same thing as context morphisms $a : \Gamma \to ( \Gamma , \phi )$ over Γ . When Γ is the empty context, we speak of global elements of the context Φ, which are the same thing as context morphisms $a : ( )  \phi$ . The expressions $( \Gamma ) \phi \in \mathop { \mathrm { C x t a n d } } \left( \Gamma \right) a \in \phi$ should be understood as counterparts of the first and second judgement in (1). It is also possible to introduce expressions $( T ) \phi = \psi \in { \mathrm { C x t } }$ and $( \boldsymbol { { \Gamma } } ) a = b \in \varPhi$ that correspond to the third and fourth judgement in (1), respectively, so that the evident counterparts of the rules in Appendix hold. The details are essentially straightforward, and hence omitted. 

Remark 1. Let Φ be a context, or a dependent context, as in (2). We also write $( x \in \Phi )$ to denote Φ itself. We then write $( x \in \phi , y \in \phi )$ for the result of duplicating $\varPhi$ and renaming the variables in the second copy to avoid clashes, so as to obtain the contex 

$$
\left(x _ {0} \in A _ {0}, x _ {1} \in A _ {1} (x _ {0}), \dots , x _ {n} \in A _ {n} (x _ {0}, \dots , x _ {n - 1}), \quad y _ {0} \in A _ {0}, y _ {1} \in A _ {1} (y _ {0}), \dots , y _ {n} \in A _ {n} (y _ {0}, \dots , y _ {n - 1})\right).
$$

The axioms for identity types are stated in Table 1. The axiom in (3) is referred to as the formation rule for identity types. It asserts that if A is a type and a, b are elements of A, then $\operatorname { I d } _ { A } ( a , b )$ is a type. We omit the subscript in expressions of the form ${ \mathrm { I d } } _ { A } ( a , b )$ when no confusion arises. If there exists an element $p \in { \mathrm { I d } } ( a , b )$ , then we say that a and b are propositionally equal. The axiom in (4) is referred to as the introduction rule for identity types. Elements of the form $\boldsymbol { \mathrm { r } } ( a ) \in \mathrm { I d } ( a , a )$ are referred to as reflexivity elements. The axioms in (5) and (6) are referred to as the elimination rule and the computation rule, respectively For brevity, we have omitted from their premisses the judgement 

$$
\left(x \in A, y \in A, u \in \operatorname{Id} (x, y), \Theta (x, y, u)\right) C (x, y, u) \in \text { Type }.
$$

In these rules we are assuming that $\Theta ( x , y , u )$ is a dependent context relative to the context $( x \in A , y \in A , u \in \operatorname { I d } ( x , y ) )$ We have highlighted the variables x, y, u in $\Theta ( x , y , u )$ in order to describe their role in the deduction rules without using substitution. All the axioms in Table 1 should be understood as being relative to a context Γ that is common to both the premisses and the conclusion of the rules, which we leave implicit for brevity. Hence, all the constructions that we perform in $\mathcal { C } ( \mathbb { T } )$ may equally well take place in one of its slices. The presence of the implicit context Γ plays a role only when stating three axioms, which we also assume as being part of the rules for identity types, expressing commutation laws between the syntax of identity types and the substitution operation. The first of these axioms is 

$$
\frac {(\Gamma , x \in A) B (x) \in \text { Type } (\Gamma , x \in A) b _ {1} (x) \in B (x) (\Gamma , x \in A) b _ {2} (x) \in B (x) (\Gamma) a \in A}{(\Gamma) \operatorname{Id} _ {B (x)} (b _ {1} (x) , b _ {2} (x)) [ a / x ] = \operatorname{Id} _ {B (a)} (b _ {1} (a) , b _ {2} (a)) \in \text { Type }}.
$$

The second of these axioms is 

$$
\frac {(\Gamma , x \in A)   B (x) \in \text { Type } \quad (\Gamma , x \in A)   b (x) \in B (x) \quad (\Gamma)   a \in A}{(\Gamma)   \mathrm{r} (b (x)) [ a / x ] = \mathrm{r} (b (a)) \in \mathrm{Id} _ {B (a)} (b (a) , b (a))}.
$$

The third axiom, which we do not spell out, asserts a similar commutation property for terms of the form $\textstyle \operatorname { J } ( a , b , p , d )$ ). The assumption of these axioms ensures that all the constructions that we perform, when regarded as taking place in one of the slices of C(<sup>T</sup>), are stable under pullbacks. 

(3) 

$$
\mathrm{r} (a) \in \operatorname{Id} _ {A} (a, a)\tag{4}
$$

$$
p \in \operatorname{Id} _ {A} (a, b) \quad (x \in A, \Theta (x, x, \mathrm{r} (x))) d (x) \in C (x, x, \mathrm{r} (x))
$$

$$
(\Theta (a, b, p)) \mathrm{J} (a, b, p, d) \in C (a, b, p)\tag{5}
$$

$$
\frac {a \in A \qquad (x \in A ,   \Theta (x , x , \mathrm{r} (x)))   d (x) \in C (x , x , \mathrm{r} (x))}{(\Theta (a , a , \mathrm{r} (a))   \mathrm{J} (a , a , \mathrm{r} (a) , d) = d (a) \in C (a , a , \mathrm{r} (a))}\tag{6}
$$

Remark 2. Expressions of the form $e ( e ^ { \prime } )$ denote the application of e to $e ^ { \prime }$ in the metatheory. For an expression e in which the variable x may appear free, we write [x]e to denote the λ-abstraction of x from e in the metatheory. As usual, we assume the η-rule and the β-rule in the metatheory. Using these rules, it is possible to show that the elimination and computation rules in (5) and (6) can be stated equivalently as 

$$
\frac {p \in \operatorname{Id} _ {A} (a , b) \qquad (x \in A , \Theta (x , x , \mathrm{r} (x)))   e \in C (x , x , \mathrm{r} (x))}{(\Theta (a , b , p))   \mathrm{J} (a , b , p , [ x ] e) \in C (a , b , p)}
$$

and 

$$
\frac {a \in A \qquad (x \in A , \Theta (x , x , \mathrm{r} (x)))   e \in C (x , x , \mathrm{r} (x))}{(\Theta (a , a , \mathrm{r} (a))   \mathrm{J} (a , a , \mathrm{r} (a) , [ x ] e) = e [ a / x ] \in C (a , a , \mathrm{r} (a))}
$$

where $e [ a / x ]$ denotes the result of substituting a for x in e. We write [ le to denote the λ-abstraction of a variable that does not appear in e. 

Remark 3. The elimination and computation rules, as stated in Table 1, generalise the standard elimination and computation rules for identity types [25]. The latter can be obtained from the former by restricting the context Θ(x, y, u) to be empty. The reason for adopting the generalised rules instead of the standard ones is related to our preference for working without assuming the axioms for 5-types. Without 5-types, the standard rules are quite weak, since they do not seem to imply the Leibniz rule for propositional equality [25], whereas our generalised rules suffice, as shown in Lemma 5. Furthermore, the generalised rules become derivable from the standard ones in the presence of 5-types, so that our development applies also to dependent type theories with standard axioms for identity types and 5-types. 

Remark 4. We do not assume the rules in (7), to which we refer as the reflection rules. 

$$
\frac {p \in \operatorname{Id} (a , b)}{a = b \in A} \qquad \frac {p \in \operatorname{Id} (a , b)}{\operatorname{r} (a) = p \in \operatorname{Id} (a , b)}.\tag{7}
$$

The first reflection rule was shown to be independent from the axioms for identity types in [12]. Note that the judgement $\boldsymbol { \mathrm { r } } ( a ) \in \mathrm { I d } ( a , b )$ , that is presupposed by the conclusion of the second reflection rule, is derivable by the first reflection rule and the standard rules concerning substitution, as given in the Appendix. The reflection rules are generally avoided, since they imply that propositional equality and definitional equality collapse into equivalent notions, which has the effect of destroying the decidability of type-checking, one of the fundamental properties of dependent type theories [11]. As shown in [15, Proposition 10.1.3] extending [32, Theorem 1.1], the reflection rules are equivalent to the following rule 

$$
p \in \operatorname{Id} (a, b) (x \in A, y \in A, u \in \operatorname{Id} (x, y), \Theta (x, y, u)) e (x, y, u) \in C (x, y, u)
$$

$$
(\Theta (a, b, p)) J (a, b, p, [ x ] e (x, x, \mathrm{r} (x))) = e (a, b, p) \in C (a, b, p)
$$

where we used the notation for λ-abstractions in the metatheory explained in Remark 2. If the computation rule for identity types in (5) is understood as a version of the $\beta \mathrm { - r u l e }$ , then this rule can be understood as a version of the η-rule. 

One fundamental fact for our development is that, as shown in [8], the axioms for identity types can be used to construct what we will refer to as identity contexts. More precisely. there are explicit definitions (which we sketch below) such that all the rules in Table 2 are derivable. Because of their similarity with the axioms for identity types, we refer to (8) as the formation rule, to (9) as the introduction rule, to (10) as the elimination rule, and to (11) as the computation rule for identity contexts. When stating these rules, we leave again implicit a context Γ , to which all the notions are assumed to be relative. For example, in the introduction rule $\varPhi$ may be assumed to be a context relative to Γ . When stating the elimination and computation rules, we are assuming that Φ has the form in (2) and using the notational conventions set in Remark 1. For 

$$
\Phi \in \mathsf {C x t} \quad a \in \Phi \quad b \in \Phi
$$

$$
\operatorname{Id} _ {\phi} (a, b) \in \mathrm{Cxt}\tag{8}
$$

$$
a \in \varPhi
$$

$$
\mathrm{r} (a) \in \operatorname{Id} _ {\phi} (a, a)\tag{9}
$$

$$
p \in \operatorname{Id} _ {\Phi} (a, b) \quad (x \in \Phi , \Theta (x, x, \mathrm{r} (x)) d (x) \in \Omega (x, x, \mathrm{r} (x))
$$

$$
(\Theta (a, b, p)) \mathrm{J} (a, b, p, d) \in \Omega (a, b, p)\tag{10}
$$

$$
a \in \varPhi (x \in \varPhi , \Theta (x, x, \mathrm{r} (x))) d (x) \in \varOmega (x, x, \mathrm{r} (x))
$$

$$
(\Theta (a, a, \mathrm{r} (a))) \mathrm{J} (a, a, \mathrm{r} (a), d) = d (a) \in \Omega (a, a, \mathrm{r} (a))\tag{11}
$$

a context Φ and a, $b \in \Phi$ , we refer to a context of the form $\textstyle \operatorname { I d } _ { \phi } ( a , b )$ as an identity context. As before, we have omitted the judgement 

$$
\left(x \in \Phi , y \in \Phi , u \in \operatorname{Id} _ {\Phi} (x, y), \Theta (x, y, u)\right) \Omega (x, y, u) \in \mathrm{Cxt}
$$

from the premisses of the elimination and computation rules. From now on, we omit the subscript from expressions of the form $\textstyle \operatorname { I d } _ { \phi } ( a , b )$ if no confusion arises. It will be convenient to fix some terminology. When we use the elimination rule as in Table 2, we will say that we are applying the elimination rule on $p \in { \mathrm { I d } } ( a , b )$ . We refer to the relative context $\varOmega ( x , y , u )$ as the eliminating context, and to d as the eliminating family. We construct the identity context of a context Φ by induction on its length. For a context of length $n = 1$ , the definition is straightforward: if ${ \Phi } = ( x \in A )$ , then elements of Φ are the same as elements of the type A, and the identity context corresponding to a, $b \in \Phi$ is given by 

$$
\operatorname{Id} _ {\Phi} (a, b) = (u \in \operatorname{Id} _ {A} (a, b)).
$$

The introduction rule (9) then reduces to the identity type introduction rule (6); whilst the elimination rule (10) may be derived from the identity type elimination rule (5) by induction on the length of the context Ω. Assuming we know how to define the identity contexts associated to contexts of length n, we can describe the identity context associated to a context of length $n + 1$ as follows. First we use the inductive hypothesis to prove Lemma 5 below. This Lemma states a very useful property, which we refer as the Leibniz rule for contexts, that is going to be used repeatedly in what follows. To prove it, we make use of the elimination and computation rules (10) and (11) for contexts of length n. 

Lemma 5. For each context Φ of length n, we can derive a rule of the form 

$$
\frac {p \in \operatorname{Id} (a , b) \quad (x \in \varPhi)   \varOmega (x) \in \operatorname{Cxt} \quad e \in \varOmega (a)}{p _ {!} (e) \in \varOmega (b)}
$$

such that 

$$
\frac {a \in \varPhi \quad e \in \varOmega (a)}{(\mathrm{r} (a)) _ {!} (e) = e \in \varOmega (a)}
$$

holds. 

Proof. We use elimination over $p \in \operatorname { I d } ( a , b )$ with 

$$
\left(x \in \Phi , y \in \Phi , u \in \operatorname{Id} (x, y), z \in \Omega (x)\right) \Omega (y) \in \mathrm{Cxt}
$$

as the eliminating context. Since we have 

$$
(x \in \Phi , z \in \Omega (x)) z \in \Omega (x)
$$

the elimination rule allows us to derive 

$$
(z \in \Omega (a)) J (a, b, p, [ x ] z) \in \Omega (b).
$$

The required term $p _ { ! } ( e )$ is defined as the result of substituting $e \in \varOmega ( a )$ for $z \in \varOmega ( a )$ in the expression J(a, b, p, [x]z), so that 

$$
p _ {!} (e) = \mathrm{J} (a, b, p, [ x ] e) \in \Omega (b).
$$

The second rule is an immediate consequence of this definition and the computation rule. <sup></sup> 

We now define the identity context of a context of length $n + 1$ . Let us assume to have a context Φ of length n as in (2), and consider a context $\varPhi ^ { \prime }$ of length $n + 1$ of the form 

$$
\Phi^ {\prime} = (x \in \Phi , x _ {n + 1} \in A _ {n + 1} (x)).\tag{12}
$$

By definition, elements $a ^ { \prime } , b ^ { \prime } \in \mathcal { P } ^ { \prime }$ have the form $a ^ { \prime } = ( a , a _ { n + 1 } )$ and $b ^ { \prime } = ( b , b _ { n + 1 } )$ , where $a , b \in \phi , a _ { n + 1 } \in A _ { n + 1 } ( a )$ , and $b _ { n + 1 } \in A _ { n + 1 } ( b )$ . We define their associated identity context to have the form 

$$
\operatorname{Id} \left(a ^ {\prime}, b ^ {\prime}\right) = \left(u \in \operatorname{Id} _ {\Phi} (a, b), u _ {n + 1} \in \operatorname{Id} _ {A _ {n + 1} (b)} \left(u _ {!} \left(a _ {n + 1}\right), b _ {n + 1}\right)\right)
$$

where we have $u _ { ! } ( a _ { n + 1 } ) \in A _ { n + 1 } ( b )$ by the following application of the Leibniz rule 

$$
\frac {u \in \operatorname{Id} _ {\varPhi} (a , b) \qquad (x \in \varPhi)   A _ {n + 1} (x) \in \text { Type } \qquad a _ {n + 1} \in A _ {n + 1} (a)}{u _ {!} (a _ {n + 1}) \in A _ {n + 1} (b)}  .
$$

This gives us the formation rule (8) for $[ { \bf d } _ { \phi ^ { \prime } } ( a ^ { \prime } , b ^ { \prime } )$ ). The corresponding introduction, elimination and computation rules are defined in a similar inductive manner. Since in the following we will need only the description of the identity contexts and the rules in Table 2, we omit the remaining details, which may be found in [8]. 

## 3. The fundamental groupoid of a context

The axioms for identity types allow us to think of a context $\varPhi$ as a space, as we explain below. To emphasize this perspective, we refer to elements of Φ as points. Given two points $a , b \in \phi$ , we refer to elements of Id(a, b) as paths from a to b. Following this idea, the context $\textstyle \operatorname { I d } ( a , b )$ can be thought of as the space of all paths from a to b. To speak of homotopies between paths, it suffices to apply the formation rule as follows: 

$$
\frac {p _ {0} \in \operatorname{Id} (a , b) \quad p _ {1} \in \operatorname{Id} (a , b)}{\operatorname{Id} (p _ {0} , p _ {1}) \in \operatorname{Cxt}}.
$$

Elements $\theta \in \operatorname { I d } ( p _ { 0 } , p _ { 1 } )$ will be referred to as homotopies from $p _ { 0 }$ to $p _ { 1 } ,$ , and two paths $p _ { 0 } \in \operatorname { I d } ( a , b )$ and $p _ { 1 } \in \operatorname { I d } ( a , b )$ will be said to be homotopic if there exists a homotopy between them. Our aim is to pursue this analogy and to define a groupoid having the points of $\varPhi$ as objects and homotopy equivalence classes of paths as maps. Because of the analogy with the definition of the fundamental groupoid of a space [23], we refer to this groupoid as the fundamental groupoid of a context. 

Lemma 6 below can the understood as expressing that paths can be composed, that there is a trivial path on each point, and that paths can be reversed. From now on, we assume to work with a fixed context Φ as in (2). We use freely the notation introduced in Remark 1 

Lemma 6. We can derive rules of the form 

$$
\frac {p \in \operatorname{Id} (a , b) \quad q \in \operatorname{Id} (b , c)}{q \circ p \in \operatorname{Id} (a , c)} \qquad \frac {a \in \varPhi}{1 _ {a} \in \operatorname{Id} (a , a)} \qquad \frac {p \in \operatorname{Id} (a , b)}{p ^ {- 1} \in \operatorname{Id} (b , a)}
$$

such that 

$$
\frac {p \in \operatorname{Id} (a , b)}{1 _ {b} \circ p = p \in \operatorname{Id} (a , b)} \quad \frac {a \in \Phi}{(1 _ {a}) ^ {- 1} = 1 _ {a} \in \operatorname{Id} (a , a)}
$$

hold. 

Proof. For the first rule, we apply the Leibniz rule as follows 

$$
\frac {q \in \operatorname{Id} (b , c) \quad (x \in \varPhi) \operatorname{Id} (a , x) \in \operatorname{Cxt} \quad p \in \operatorname{Id} (a , b)}{q _ {!} (p) \in \operatorname{Id} (a , c)}
$$

and define $q \circ p = _ { \mathrm { d e f } } q _ { ! } ( p ) \in \mathrm { I d } ( a , c )$ . For the second rule, we use the introduction rule, and simply define $1 _ { a } = _ { \mathrm { d e f } } { \mathrm { ~ r } } ( a ) \in$ $\textstyle \operatorname { I d } ( a , a )$ . For the third rule, we apply the elimination rule on $p \in \operatorname { I d } ( a , b )$ , with 

$$
(x \in \Phi , y \in \Phi , u \in \operatorname{Id} (x, y)) \operatorname{Id} (y, x) \in \mathrm{Cxt}
$$

as the eliminating context, and $\boldsymbol { \mathrm { r } } ( \boldsymbol { x } ) \in \mathrm { I d } ( \boldsymbol { x } , \boldsymbol { x } )$ as the eliminating family. Hence, we can define 

$$
p ^ {- 1} = _ {\text { def }} \mathrm{J} (a, b, p, [ x ] \mathrm{r} (x)) \in \operatorname{Id} (b, a).
$$

The computation rule implies the other rules. <sup></sup> 

Lemma 7. Let $p _ { 0 } , p _ { 1 } \in \operatorname { I d } ( a , b )$ and $q _ { 0 } , q _ { 1 } \in \mathrm { I d } ( b , c )$ . We can derive rules of the form 

$$
\frac {\phi \in \operatorname{Id} (p _ {0} , p _ {1}) \quad \psi \in \operatorname{Id} (q _ {0} , q _ {1})}{\psi \circ \phi \in \operatorname{Id} (q _ {0} \circ p _ {0} , q _ {1} \circ p _ {1})} \qquad \frac {\phi \in \operatorname{Id} (p _ {0} , p _ {1})}{\phi^ {*} \in \operatorname{Id} (p _ {0} ^ {- 1} , p _ {1} ^ {- 1})}
$$

such that 

$$
\frac {p \in \operatorname{Id} (a , b) \quad q \in \operatorname{Id} (b , c)}{1 _ {q} \circ 1 _ {p} = 1 _ {q \circ p} \in \operatorname{Id} (q \circ p , q \circ p)} \qquad \frac {p \in \operatorname{Id} (a , b)}{(1 _ {p}) ^ {*} = 1 _ {p} \in \operatorname{Id} (p , p)}
$$

hold. 

Proof. For the first rule, use elimination over $\phi \in \mathrm { I d } ( p _ { 0 } , p _ { 1 } )$ and $\psi \in \mathrm { I d } ( q _ { 0 } , q _ { 1 } )$ , and Lemma 6. For the second rule, use elimination over $\phi \in \mathrm { I d } ( p _ { 0 } , p _ { 1 } )$ and Lemma 6. <sup></sup> 

Lemma 8. We can derive rules of the form 

$$
\begin{array}{c c} \hline p \in \operatorname{Id} (a, b) \qquad q \in \operatorname{Id} (b, c) \qquad r \in \operatorname{Id} (c, d) \\ \hline \alpha_ {p, q, r} \in \operatorname{Id} ((r \circ q) \circ p, r \circ (q \circ p)) \\ \frac {p \in \operatorname{Id} (a , b)}{\phi_ {p} \in \operatorname{Id} (1 _ {b} \circ p , p)} & \frac {p \in \operatorname{Id} (a , b)}{\psi_ {p} \in \operatorname{Id} (p \circ 1 _ {a} , p)} \\ \frac {p \in \operatorname{Id} (a , b)}{\sigma_ {p} \in \operatorname{Id} (p ^ {- 1} \circ p , 1 _ {a})} & \frac {p \in \operatorname{Id} (a , b)}{\tau_ {p} \in \operatorname{Id} (p \circ p ^ {- 1} , 1 _ {b})} \end{array}
$$

such that 

$$
\begin{array}{c c} \frac {p \in \operatorname{Id} (a , b) \qquad q \in \operatorname{Id} (b , c)}{\alpha_ {p , q , 1 _ {c}} = 1 _ {q \circ p} \in \operatorname{Id} (q \circ p , q \circ p)} \\ \frac {a \in \varPhi}{\phi_ {1 _ {a}} = 1 _ {1 _ {a}} \in \operatorname{Id} (1 _ {a} , 1 _ {a})} & \frac {a \in \varPhi}{\psi_ {1 _ {a}} = 1 _ {1 _ {a}} \in \operatorname{Id} (1 _ {a} , 1 _ {a})} \\ \frac {a \in A}{\sigma_ {1 _ {a}} = 1 _ {1 _ {a}} \in \operatorname{Id} (1 _ {a} , 1 _ {a})} & \frac {a \in A}{\tau_ {1 _ {a}} = 1 _ {1 _ {a}} \in \operatorname{Id} (1 _ {a} , 1 _ {a})} \end{array}
$$

hold. 

Proof. For $\alpha _ { p , q , r }$ use elimination over $r \in \operatorname { I d } ( c , d )$ . For $\phi _ { p }$ we can define $\phi _ { p }$ to be $1 _ { p }$ by Lemma 6. For $\psi _ { p }$ use elimination over $p \in { \mathrm { I d } } ( a , b )$ . For $\sigma _ { p }$ and $\tau _ { p }$ use elimination over $p \in \operatorname { I d } ( { \bar { a } } , b )$  

Let $a , b \in { \mathcal { P } }$ . An application of Lemma 6, taking Φ therein to be $\textstyle \operatorname { I d } _ { \phi } ( a , b )$ , shows that homotopy of paths is a reflexive, symmetric, and transitive relation on the set of paths from a to b. We write [a, b] for the quotient set, and $[ p ] : a  b$ for the equivalence class of a path $p \in \operatorname { I d } ( a , b )$ . We can now define the fundamental groupoid $\mathcal { F } ( \phi )$ associated to Φ. The objects of $\mathcal { F } ( \phi )$ are the global elements of Φ. The maps from a to b in ${ \mathcal { F } } ( \phi )$ are equivalence classes of paths $[ p ] : a  b .$ Composition, identities, and inverses in ${ \mathcal { F } } ( \phi )$ are defined by letting 

$$
[ q ] \circ [ p ] = _ {\mathrm{def}} [ q \circ p ], \quad 1 _ {a} = _ {\mathrm{def}} [ 1 _ {a} ], \quad [ p ] ^ {- 1} = _ {\mathrm{def}} [ p ^ {- 1} ].
$$

These operations are well-defined by Lemma 7. To establish the axioms for a category, we need to show 

$$
[ r \circ (q \circ p) ] = [ (r \circ q) \circ p ], \quad [ 1 _ {b} \circ p ] = [ p ], \quad [ p \circ 1 _ {a} ] = [ p ]\tag{13}
$$

and to establish the additional axioms for a groupoid, we need to show 

$$
[ p ^ {- 1} \circ p ] = [ 1 _ {a} ], \quad [ p \circ p ^ {- 1} ] = [ 1 _ {b} ].\tag{14}
$$

For (13), we need homotopies $\alpha \in \mathrm { I d } ( r \circ ( q \circ p ) , ( r \circ q ) \circ p ) , \phi \in \mathrm { I d } ( 1 _ { b } \circ p , p )$ , and $\psi \in \mathrm { I d } ( p \circ 1 _ { a } , p )$ . For (14), we need homotopies $\sigma \in \mathsf { I d } ( p ^ { - 1 } \circ p , 1 _ { a } )$ and $\tau \in \mathrm { I d } ( p \circ p ^ { - 1 } , 1 _ { b } )$ . All of these are provided by Lemma 8. We now show that this construction extends to a functor. Recall that we write Gpd for the category of small groupoids and functors. 

Proposition 9. Let <sup>T</sup> be a dependent type theory with axioms for identity types. The function mapping a context Φ to its fundamental groupoid ${ \mathcal { F } } ( \phi )$ extends to a functor $\mathcal { F } : \mathcal { C } ( \mathbb { T } ) \to \mathbf { G p d } .$ 

Proof. We need to define a functor $\mathcal { F } ( f ) : \mathcal { F } ( \phi )  \mathcal { F } ( \psi )$ for every context morphism $f : \phi  \psi$ . On objects, $\mathcal { F } ( f )$ sends $a \in { \mathcal { F } } ( \phi )$ to $f ( a ) \in { \mathcal { F } } ( \psi )$ . On maps, $\mathcal { F } ( f )$ sends $[ p ] : a \to b \mathrm { t o } [ f ( p ) ] : f ( a ) \to f ( b )$ , where $f ( p ) \in \operatorname { I d } ( f ( a ) , f ( b ) )$ is defined using the elimination rule by letting 

$$
f (p) = \mathrm{J} (a, b, p, [ x ] 1 _ {f x}) \in \operatorname{Id} (f (a), f (b)),\tag{15}
$$

so that 

$$
f (1 _ {a}) = 1 _ {f a} \in \operatorname{Id} (f (a), f (a)).\tag{16}
$$

It is routine to check that the action of $\mathcal { F } ( f )$ on maps is well-defined. To show that $\mathcal { F } ( f )$ is a functor amounts to verifying the equations 

$$
[ f (q \circ p) ] = [ f (q) \circ f (p) ], \quad [ f (1 _ {a}) ] = [ 1 _ {f (a)} ].
$$

For the first equation, elimination on $q \ \in \ \operatorname { I d } ( b , c )$ can be used to exhibit the required homotopy between $f ( q \circ p )$ and $f ( q ) \circ f ( p )$ . For the second equation, use (16). We have therefore defined $\mathcal { F } : \mathcal { C } ( \mathbb { T } ) $ Gpd on obiects and maps. Thus. it remains to check that it is a functor. We begin by checking 

$$
\mathcal {F} (g \circ f) = \mathcal {F} (g) \circ \mathcal {F} (f).
$$

It is clear that ${ \mathcal { F } } ( g \circ f )$ and ${ \mathcal { F } } ( g ) \circ { \mathcal { F } } ( f )$ have the same action on objects. To show that they coincide on maps, we need to show that we have a homotopy between $g ( f ( p ) )$ ) and $( g f ) ( p )$ for every $p \in { \mathrm { I d } } ( a , b )$ . By (15), we have 

$$
g (f (p)) = \mathrm{J} (f (a), f (b), f (p), [ x ] 1 _ {g (x)}) \in \operatorname{Id} (\operatorname{gf} (a), \operatorname{gf} (b))
$$

and 

$$
(g f) (p) = \mathrm{J} (a, b, p, [ x ] 1 _ {g f (x)}) \in \operatorname{Id} (g f (a), g f (b)).
$$

The required homotopy can be obtained by the elimination rule on $p \in { \mathrm { I d } } ( a , b )$ . To conclude the proof, it suffices to check that 

$$
\mathcal {F} (1 _ {\phi}) = 1 _ {\mathcal {F} (\phi)}.
$$

As before, it is clear that $\mathcal { F } ( 1 _ { \phi } )$ is the identity on objects. To check that it is the identity on maps, it suffices to show that $[ p ] : a  b$ and $[ 1 _ { \phi } ( p ) ] : a  b$ are the same equivalence classes, which can be proved by the elimination rule on $p \in \operatorname { I d } ( a , b )$ .  

## 4. The identity type weak factorisation system

Let us recall the notion of a weak factorisation system [4]. For this, we need some terminology and notation. Let E be a category. Given maps $f : A  B$ and $g : C \to D$ in E , we say that f has the left lifting property with respect to g, or that g has the right lifting property with respect to f , if every commutative diagram of the form 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/a6a9948645687f149f3be4bfcfb80cbb542a7e1160dbcc862d37543a83b6891e.jpg)


has a diagonal filler, that is to say is a map j : B → C making the diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/e74573a9c1fde9268950ceae07eeb989ed57d789ee3ddccd0a62e483f183c2bd.jpg)


commute. We write $f \pitchfork g$ to denote this situation. For a class of maps M, we define $\mathcal { M } ^ { \mathrm { \uparrow \uparrow } }$ to be the class of maps having the right lifting property with respect to every map in M. Similarly, we define <sup>t</sup>M to be the class of maps having the left lifting property with respect to every map in M. A weak factorisation system on E consists of a pair of classes of maps $( { \mathcal { A } } , { \mathcal { B } } )$ such that the following hold. 

(1) Every map f admits a factorisation $f = p i$ with $i \in \mathcal { A }$ and $p \in { \mathcal { B } }$ 

(2) $\mathcal { A } ^ { \pitchfork } = \mathcal { B }$ and ${ \mathcal { A } } = { \mathrm { ~ } } ^ { \pitchfork } { \mathcal { B } } .$ 

We refer to (1) as the Factorisation Axiom and to (2) as the Weak Orthogonality Axiom. Elements of A and B will be also referred to as A-maps and B-maps, respectively. For more information on weak factorisation systems, see [16, Appendix D]. 

Let us now return to consider the dependent type theory <sup>T</sup> and its classifying category ${ \mathcal { C } } ( \mathbb { T } )$ ). Recall from Section 2 that a display map is a context morphism of the form $( { \cal { T } } , x \in A )  { \cal { T } }$ , obtained by forgetting the variable $x \in A$ We write D for the set of display maps in C(<sup>T</sup>). Our main result is the following. 

Theorem 10. Let <sup>T</sup> be dependent type theory with axioms for identity types. The pair $( { \mathcal { A } } , { \mathcal { B } } )$ , where ${ \mathcal { A } } = _ { \mathrm { d e f } } { } ^ { \mathrm { n } } { \mathcal { D } }$ and $\mathcal { B } = _ { \mathrm { d e f } } \mathcal { A } ^ { \hbar }$ forms a weak factorisation system on C(<sup>T</sup>). 

Let us emphasize that identity types are not involved in the definition of the classes of maps A and B. They are, however, used extensively in the proof that these classes of maps satisfy the axioms for a weak factorisation system. As usual in the proof of the existence of a weak factorisation system, the difficulties are concentrated in one particular step of the proof. Lemma 11 is the key step in our case, with the proof of Theorem 10 following from it by standard arguments in the theory of weak factorisation systems. To prove Lemma 11, it is convenient to work with the equivalent formulation of the rules for identity contexts given in Table 3. The equivalence between the sets of rules in Table 2 and in Table 3 follows by standard properties of substitution. As before, we use the notational convention stipulated in Remark 1. Also recall that a dependent projection is a context morphism of the form $( \Gamma , \phi )  \Gamma$ , defined by projecting away the variables in Φ, where Γ is a context and $\varPhi$ is context relative to Γ . 

Lemma 11. Every map f admits a factorisation $f = p i ,$ , where $i \in \mathcal { A }$ and p is a dependent projection 

Variable-based rules for identity contexts 

$\begin{array}{c}\frac{\Phi\in\mathrm{Cxt}}{(x\in\Phi,y\in\Phi)\operatorname{Id}_{\Phi}(x,y)\in\mathrm{Cxt}}\\ \frac{\Phi\in\mathrm{Cxt}}{(x\in\Phi)\operatorname{r}(x)\in\operatorname{Id}_{\Phi}(x,x)}\\ \frac{(x\in\Phi,\Theta(x,x,\operatorname{r}(x)))d(x)\in\Omega(x,x,\operatorname{r}x)}{(x\in\Phi,y\in\Phi,u\in\operatorname{Id}_{\Phi}(x,y),\Theta(x,y,u))J(x,y,u,d)\in\Omega(x,y,u)}\\ \frac{(x\in\Phi,\Theta(x,x,\operatorname{r}(x)))d(x)\in\Omega(x,x,\operatorname{r}(x))}{((x\in\Phi,\Theta(x,x\operatorname{r}(x))))J(x,x,\operatorname{r}(x),d)=d(x)\in\Omega(x,x,\operatorname{r}(x))}\\ \end{array}$ 

Proof. For $f : \phi  \psi$ , define $\begin{array} { r } { \mathbf { I d } ( f ) = _ { \mathrm { d e f } } \left( x \in \varPhi , y \in \varPsi , u \in \mathrm { I d } _ { \psi } ( f x , y ) \right) } \end{array}$ . The required factorisation is defined as follows: 

$$
\Phi \xrightarrow {i _ {f}} \operatorname{Id} (f) \xrightarrow {p _ {f}} \Psi ,\tag{17}
$$

where $i _ { f } = _ { \mathrm { d e f } } ~ ( x , f x , 1 _ { f x } )$ and $p _ { f } = ( y )$ . Apart from the ordering of the variable declarations $x \in \Phi$ and $y \in \psi$ , which is clearly unessential, p is a dependent projection, as required. Hence, we only need to show that $i _ { f } \in \mathcal { A } .$ . This amounts to showing that it has the left lifting property with respect to all display maps. This amounts to providing diagonal fillers for every diagram of the form 

$$
\begin{array}{c} \Phi \longrightarrow (v \in \varLambda , z \in D (v)) \\ \Bigg \downarrow \qquad \qquad \qquad \qquad \qquad \qquad \Bigg \downarrow \\ \operatorname{Id} (f) \longrightarrow (v \in \varLambda). \end{array}
$$

Since display maps are closed under pullback [26, Lemma 6.3.2], it suffices to show that we can define a diagonal filler for every diagram of the form 

$$
\begin{array}{c} \Phi \longrightarrow (\operatorname{Id} (f), z \in C (x, y, u)) \\ \Biggl \downarrow \qquad \qquad \qquad \qquad \qquad \qquad \qquad \Biggl \downarrow \\ \operatorname{Id} (f) = \operatorname{Id} (f). \end{array}
$$

The right-hand side display map gives us a dependent type $C ( x , y , u )$ relative to $\mathrm { I d } ( f ) = ( x \in \phi , y \in \varPsi , u \in \mathrm { I d } ( f ) )$ ). By the commutativity of the diagram, the top horizontal map gives us a dependent element $d ( x ) \in C ( x , f x , 1 _ { f x } )$ relative to $( x \in \Phi )$ . We can derive 

$$
(x \in \Phi , y _ {0} \in \Psi , y _ {1} \in \Psi , v \in \operatorname{Id} (y _ {0}, y _ {1}), \Theta (y _ {0}, y _ {1}, v)) C (x, y _ {1}, v \circ u) \in \text { Type },
$$

where $\theta ( y _ { 0 } , y _ { 1 } , v ) = ( u \in \mathrm { I d } ( f x , y _ { 0 } ) , z \in C ( x , y _ { 0 } , u ) )$ . By the definitional equality $1 _ { y } \circ u = u \in \mathrm { I d } ( f ( x ) , y _ { 0 } )$ , proved in Lemma 6, we have 

$$
\left(x \in \Phi , y \in \Psi , \Theta (y, y, 1 _ {y})\right) z \in C (x, y, 1 _ {y} \circ u).
$$

By the elimination rule applied to $v \in \mathrm { I d } ( y _ { 0 } , y _ { 1 } )$ , we obtain 

$$
(x \in \Phi , y _ {0} \in \Psi , y _ {1} \in \Psi , v \in \operatorname{Id} (y _ {0}, y _ {1}), \Theta (y _ {0}, y _ {1}, v)) J (y _ {0}, y _ {1}, v, [ \_ ] z) \in C (x, y _ {1}, v \circ u).
$$

We then obtain 

$$
\left(x \in \varPhi , y \in \varPsi , u \in \mathrm{Id} (f x, y), z \in C (x, f x, 1 _ {f x})\right) n (x, y, u, z) \in C (x, y, u \circ 1 _ {f x})
$$

where $n ( x , y , u , z ) = _ { \mathrm { d e f } } \operatorname { J } ( f x , y , u , z )$ . We can now substitute d(x) for z and obtain 

$$
(x \in \Phi , y \in \Psi , u \in \operatorname{Id} (f x, y)) n (x, y, u, d (x)) \in C (x, y, u \circ 1 _ {f x}).
$$

Let us now recall that by Lemma 8 we have $\psi _ { u } \in \mathrm { I d } ( u \circ 1 _ { f x } , u )$ . Hence, we can apply Lemma 5 and obtain 

$$
(x \in \Phi , y \in \Psi , u \in \operatorname{Id} (f x, y)) (\psi_ {u}) _ {!} (n (x, y, u, d (x))) \in C (x, y, u).
$$

We claim that $j = _ { \mathrm { d e f } } \left( x , y , u , ( \psi _ { u } ) _ { ! } ( n ( x , y , u , d ( x ) ) ) \right)$ ) provides the required filler, fitting in the diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/7bccbe9881265d5aab74858efb4f79359bcbe49afb13fc19a76c2e7c724b97fe.jpg)


The commutativity of the bottom triangle is evident. The commutativity of the top triangle follows by the chain of definitional equalities 

$$
\begin{array}{r l} (\psi_ {1 _ {f x}})! (n (x, f x, 1 _ {f x}, d (x))) & = n (x, f x, 1 _ {f x}, d (x)) \\ & = \mathrm{J} (f x, f x, 1 _ {f x}, [ \_ ] d (x)) \\ & = d (x). \end{array}
$$

Here, we used Lemma 6, the definition of $n ,$ and the elimination rule for identity types. The commutativity of the bottom triangle is immediate. <sup></sup> 

Proof of Theorem 10. Since $\mathcal { D } \subseteq \mathcal { B }$ and B is closed under composition, B contains all dependent projections. The Factorisation Axiom then follows from Lemma 11. For the Weak Orthogonality Axiom, observe that $\mathcal { A } ^ { \pitchfork } = \mathcal { B }$ by the very definition of B in Theorem 10. So, we only need to show that ${ \mathcal { A } } = { } ^ { \pitchfork } { \mathcal { B } }$ . Since ${ \mathcal { D } } \subseteq { \mathcal { B } }$ , we have ${ } ^ { \dag } { \mathcal { B } } \subseteq { } ^ { \dag } { \mathcal { D } }$ , and s $r ^ { \mathrm { ~ t ~ } } \mathcal { B } \subseteq \mathcal { A }$ Thus, it remains to prove that ${ \mathcal { A } } \subseteq { ^ { \pitchfork } \mathcal { B } }$ . Observe that every map in A has the left lifting property with respect to every dependent projection. This is because maps in A have the left lifting property with respect to display maps, and dependent projections are composites of display maps. The required inclusion ${ \mathcal { A } } \subseteq { ^ { \pitchfork } { \mathcal { B } } }$ amounts to showing that every map in A has the left lifting property with respect to every map in B. This follows from the fact that every map in A has the left lifting property with respect to every dependent projection, which we observed above, and the fact that every map in B is a retract of a dependent projection, which follows from Lemma 11 and the Retract Argument [13, Lemma 1.1.9]. <sup></sup> 

Let us illustrate what happens when we apply the factorisation of Lemma 11 to the identity map $\mid _ { \phi } : \phi  \phi$ . The factorisation in (17) becomes 

$$
\Phi \xrightarrow {i} \operatorname{Id} (\Phi) \xrightarrow {p} \Phi ,
$$

where $\mathrm { I d } ( \phi ) = _ { \mathrm { d e f } } ( x \in \phi , y \in \phi , u \in \mathrm { I d } ( x , y ) )$ ), and the maps i and p are defined by letting $i = _ { \mathrm { d e f } } \left( x , x , 1 _ { x } \right)$ and $p = _ { \mathsf { d e f } } \left( y \right)$ respectively. Let us consider a diagram of the form 

$$
\begin{array}{c} \Phi \xrightarrow {} (\operatorname{Id} (\Phi), z \in C (x, y, u)) \\ \Biggl \downarrow_ {i} \\ \operatorname{Id} (\Phi) \xlongequal {} \operatorname{Id} (\Phi) \end{array}
$$

where $C ( x , y , u )$ is a type relative to the context Id(Φ). By the commutativity of the diagram, the top horizontal map gives us a dependent element $d ( x ) ~ \in ~ C ( x , x , \operatorname { r } ( x ) )$ relative to $( x ~ \in ~ \phi )$ . By the elimination rule, we can deduce that $\operatorname { J } ( x , y , u , d ) \in C ( x , y , u )$ . We can therefore define a filler j 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/0a0c7ba4ebedde31143150f54f01553d2850ba0e3338c4d79017a979469bf362.jpg)


by letting $j = _ { \mathrm { d e f } } \ ( x , y , u , \operatorname { J } ( x , y , u , d ) )$ . The commutativity of the top triangle follows from the computation rule, while the commutativity of the bottom triangle is immediate. This is the key idea underpinning the semantics of identity types in weak factorisation systems introduced in [2]. 

Remark 12. The identity type weak factorisation system is not a functorial weak factorisation system. This would entai having operations mapping commutative squares 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/163e321fabe8ffcf616864ab28609f52c16b5899517ac5f52dc77daf21bb0ec0.jpg)


into commutative diagrams 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/dec94b5c04265a45268bb7e7ebaa0754d94990baf1ea68a5ab150f3d3ffd9a0a.jpg)


(18) 


subject to the functoriality conditions


$$
\operatorname{Id} _ {1 _ {\phi}, 1 _ {\phi^ {\prime}}} = 1 _ {\operatorname{Id} (u)} \quad \operatorname{Id} _ {h, k} \circ \operatorname{Id} _ {f, g} = \operatorname{Id} _ {h f, k g}.\tag{19}
$$

We can use the identity elimination rules to define maps $\mathrm { I d } _ { f , g } : \mathrm { I d } ( u )  \mathrm { I d } ( v )$ making the diagram in (18) commute and satisfying the first functoriality condition in (19). However, these maps need not satisfy the second functoriality condition in (19) strictly, but only up to propositional equality. To see why this is, let us consider the following situation: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/9bb02b1bb2a6f3415768df7b1c36e65fe553a951be225c15a615f309e0567770.jpg)


The maps $\mathrm { I d } _ { f , f } : \mathrm { I d } ( \phi )  \mathrm { I d } ( \psi )$ and $\operatorname { I d } _ { g , g } : \operatorname { I d } ( \psi )  \operatorname { I d } ( E )$ are defined as in Eq. (15) of Proposition 9. Their composite will not in general be equal to the map $\mathrm { I d } _ { g f , g f } : \mathrm { I d } ( \varPhi )  \mathrm { I d } ( \varXi )$ ), but only pointwise propositionally equal. 

## 5. Characterisation and applications

We provide an explicit characterisation of the maps in the classes A and B of the identity type weak factorisation system established in Theorem 10. For this, we introduce some terminology, which is inspired by concepts of two-dimensional category theory [3,18,31]. We define a context morphism $f : \phi  \psi$ to be a type-theoretic injective equivalence if we can derive a judgement 

$$
(y \in \Psi) s (y) \in \Phi
$$

such that we can derive also judgements of the form 

$$
\begin{array}{l} (x \in \varPhi)   x = s (f (x)) \in \varPhi , \\ (y \in \varPsi)   \varepsilon_ {y} \in \mathrm{Id} _ {\varPsi} (f (s (y)), y), \\ (x \in \varPhi)   \varepsilon_ {f (x)} = 1 _ {f (x)} \in \mathrm{Id} _ {\varPsi} (f (x), f (x)). \end{array}\tag{20}
$$

(21) 

(22) 

We say that $f : \phi  \psi$ is a type-theoretic normal isofibration if we can derive a judgement 

$$
\left(x \in \Phi , y \in \Psi , u \in \operatorname{Id} (f (x), y)\right) j (x, y, u) \in \Phi
$$

such that we can also derive judgements of the following form 

(23) 

(24) 

Although the identity type weak factorisation system is not to be functorial, we can follow the argument used to characterise the maps of a functorial weak factorisation system in [27, Section 2.4] to establish Lemma 13. 

Lemma 13. Let $f : \phi  \psi$ be a context morphism. 

(i) $f \in \mathcal A$ if and only if f is a type-theoretic injective equivalence. 

(ii) $f \in \mathcal { B } \ : i$ f and only if f is a type-theoretic normal isofibration. 

Proof. Recall that by Lemma 11 every map $f : \phi  \psi$ admits a factorisation 

$$
\Phi \xrightarrow {i _ {f}} \operatorname{Id} (f) \xrightarrow {p _ {f}} \Psi ,
$$

where $i _ { f } ~ \in ~ \mathcal { A }$ and $p _ { f } ~ \in ~ \mathcal { B }$ . Let us prove (i). Define $\mathcal { A } ^ { \prime }$ to be the class of maps $f : \phi \to \psi$ such that the commutative diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/122ee7773eface66c81f5ab5385faf8e700ffd166c1d22daedd7a1603afb1a50.jpg)


(25) 

has a diagonal filler. We claim that $\mathcal { A } = \mathcal { A } ^ { \prime }$ . To show $\mathcal { A } \subseteq \mathcal { A } ^ { \prime } ,$ , let $f : \phi  \psi$ be in A. The diagram in (25) has a diagonal filler since $f \in \mathcal A$ and $p _ { f } \in { \mathcal { B } }$ . To show $\mathcal { A } ^ { \prime } \subseteq \mathcal { A } , \mathrm { l e t } f : \phi \to \varPsi$ be in $\mathcal { A } ^ { \prime }$ , and assume to have a diagonal filler j : $\psi  \operatorname { I d } ( f )$ for the diagram in (25). We can then exhibit f as a retract of $i _ { f }$ by the diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/e2ae0052de9fed7476314ece2f397be7cae9cc5b3457e4be5e098f5d5214e0e6.jpg)


We have that $i _ { f } \in \mathcal A .$ . Since the class ${ \mathcal A } ,$ being defined by a weak orthogonality condition, is closed under retracts, we have $f \in \mathcal A$ . To conclude the proof, it is sufficient to observe that f is an injective equivalence if and only $\mathrm { i f } f \in \mathcal { A } ^ { \prime }$ . This involves unfolding the definitions of the context Id(f ) and of the morphism $i _ { f } : \phi \to \operatorname { I d } ( f )$ . For the proof of (ii), let $\mathcal { B } ^ { \prime }$ be the class of maps $f : \phi  \psi$ such that the commutative diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/8718f50404cff67db37f0b3155f4b6067c9be13cd96a844ab2b128e8188db1c3.jpg)


has a diagonal filler. The rest of argument follows along the lines of the one used to establish (i) and hence we omit it. <sup></sup> 

We give two applications of Lemma 13. To motivate our first application, let us recall that, given a weak factorisation system (A, B) on a category E with finite products, it is possible to define a homotopy relation between maps of E by thinking of A and B as if they were the classes of acyclic cofibrations and of fibrations of a Quillen model structure on $\varepsilon .$ For convenience, let us assume that the weak factorisation system comes together with an explicitly chosen factorisation of diagonal maps $\Delta _ { X } : X \to X \times X$ as an $\mathcal { A } \mathrm { - m a p } i _ { X } : X  X ^ { I }$ followed by a B-map $p _ { X } : X ^ { I } \to X \times X$ . We may then define two maps $f : X \to Y$ and $g : X \to Y$ to be homotopic if there exists a map $h : X \to Y ^ { I }$ such that the diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/8a6236636d15b5bb03e6c731a032aa151f1f4207862b8095c80d47c8a2340b77.jpg)


commutes. In the case of the identity type weak factorisation system, an explicit choice of factorisations of diagonal maps is given by 

$$
\Phi \xrightarrow {i} \operatorname{Id} (\Phi) \xrightarrow {p} (x \in \Phi , y \in \Phi)
$$

where the maps i and p are given by $i = _ { \mathrm { d e f } } \left( x , x , 1 _ { x } \right)$ and $p = _ { \mathrm { d e f } } \left( x , y \right)$ , respectively. It follows that two maps $f , g \colon \phi $ Ψ in the classifying category C(<sup>T</sup>) are homotopic if and only if we can derive a judgement $( x \in \phi ) p ( x ) \in { \mathrm { I d } } ( f ( x ) , g ( x ) )$ expressing their pointwise propositional equality. The homotopy relation induced by a weak factorisation system (A, B) can always be shown to be reflexive and symmetric. However, without further assumptions on the weak factorisation system we may not be able to show that it is transitive. One assumption that ensures transitivity is that pullbacks of A-maps in along B-maps are again A-maps. In our example, the classifying category C(<sup>T</sup>) does not have arbitrary pullbacks, but it does admit pullbacks along dependent projections [26, Section 6], which are B-maps. The closure property of A-maps stated in Proposition 14, however, suffices to show that the homotopy relation for the identity type weak factorisation system is transitive, as an easy calculation shows 

Proposition 14. Pullbacks of A-maps along dependent projections are A-maps. 

Proof. By Lemma 13, the claim follows once we show that, for a pullback diagram of form 

$$
\begin{array}{c} (x \in \varPhi , z \in \varOmega (f (x)) \longrightarrow (x \in \varPhi) \\ g \Biggl \downarrow \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \Biggl \downarrow f \\ (y \in \varPsi , z \in \varOmega (y)) \longrightarrow (y \in \varPsi) \end{array}
$$

$$
g = (f (x), z)
$$

$$
(y \in \Psi) s (y) \in \Phi
$$

and the judgements in (20)–(22). Our first step in showing that g is an injective equivalence will be to construct a judgement 

$$
(y \in \varPsi , z \in \varOmega (y)) t (y, z) \in (x \in \varPhi , z \in \varOmega (f (x))
$$

satisfying $( x \in \phi , z \in \varOmega ( \mathscr { x } ) ) t g ( x , z ) = ( x , z ) \in ( x \in \varPhi , z \in \varOmega ( x ) )$ . Now, to give t is equivalently to give judgements 

$$
\begin{array}{l} (y \in \varPsi , z \in \varOmega (y)) t _ {1} (y, z) \in \varPhi , \\ (y \in \varPsi , z \in \varOmega (y)) t _ {2} (y, z) \in \varOmega (f (t _ {1} (y, z))). \end{array}
$$

So we define $t _ { 1 } ( y , z ) = _ { \mathrm { d e f } } s ( y )$ . Now must give an element $t _ { 2 } ( y , z ) \in \varOmega ( f s y )$ . We obtain this by substituting $z \in \varOmega ( y )$ along $\varepsilon _ { y } ^ { - 1 } \in \operatorname { I d } ( y , f s y )$ using the Leibniz rule: 

$$
(y \in \Psi , z \in \Omega (y)) t _ {2} (y, z) = _ {\text { def }} (\varepsilon_ {y} ^ {- 1}) _ {!} (z) \in \Omega (f (t _ {1} (y, z))).
$$

Observe that we have 

$$
\begin{array}{r l} {t g (x, z)} & {= t (f x, z)} \\ & {= (t _ {1} (f x, z), t _ {2} (f x, z))} \\ & {= (s f x, (\varepsilon_ {f x} ^ {- 1}) _ {!} (z))} \\ & {= (x, (1 _ {f x}) _ {!} (z))} \\ & {= (x, z)} \end{array}
$$

as required. We now come to the second step in the proof, which is to construct a judgement 

$$
(y \in \Psi , z \in \Omega (y)) \delta_ {(y, z)} \in \operatorname{Id} (\operatorname{gt} (y, z), (y, z))
$$

satisfying $( x \in \boldsymbol { \varPhi } , z \in \varOmega \left( f x \right) ) \delta _ { ( f x , z ) } = 1 _ { ( f x , z ) } \in \mathrm { I d } ( ( f x , z ) , ( f x , z ) )$ . Now, to give δ is the same as to give a judgement 

$$
(y \in \varPsi , z \in \varOmega (y))   \delta (y, z) \in \operatorname{Id} \big ((f s y, (\varepsilon_ {y} ^ {- 1}) _ {!} (z)), (y, z) \big).
$$

By the description of identity contexts in Section 2, to give this is equally well to give a pair of judgements 

$$
\begin{array}{l} (y \in \varPsi ,   z \in \varOmega (y))   \delta_ {1} (y, z) \in \mathrm{Id} (f s y, y) \\ (y \in \varPsi ,   z \in \varOmega (y))   \delta_ {2} (y, z) \in \mathrm{Id} \big (\delta_ {1} (y, z)! (\varepsilon_ {y} ^ {- 1}) _ {!} (z), z \big). \end{array}
$$

So we define $\delta _ { 1 } ( y , z ) = _ { \mathrm { d e f } } \varepsilon ( y )$ . We must now give an element 

$$
\delta_ {2} (y, z) \in \operatorname{Id} ((\varepsilon_ {y}) _ {!} (\varepsilon_ {y} ^ {- 1}) _ {!} (z), z).
$$

For this, let us show that we can derive a rule of the form 

$$
\frac {p \in \operatorname{Id} (a , b) \qquad (x \in \varPhi)   \varOmega (x) \in \mathrm{Cxt} \qquad e \in \varOmega (b)}{\gamma_ {p} (e) \in \operatorname{Id} ((p) _ {!} (p ^ {- 1}) _ {!} (e) , e)}
$$

such that 

$$
\frac {a \in \varPhi \quad e \in \varOmega (a)}{\gamma_ {1 _ {a}} (e) = 1 _ {e} \in \operatorname{Id} (e , e)}.
$$

By elimination on $p \in { \mathrm { I d } } ( a , b )$ , we define 

$$
\gamma_ {p} (e) = _ {\text { def }} \mathrm{J} (a, b, p, [ x ] 1 _ {e}) \in \operatorname{Id} ((p) _ {!} (p ^ {- 1}) _ {!} (e), e).
$$

Indeed, Lemma 6 implies that for $x \in \phi$ and $z \in \varOmega ( x )$ , we have 

$$
\begin{array}{r l} (1 _ {x}) _ {!} (1 _ {x} ^ {- 1}) _ {!} (z) & = (1 _ {x} ^ {- 1}) _ {!} (z) \\ & = (1 _ {x}) _ {!} (z) \\ & = z. \end{array}
$$

We can then define $\delta _ { 2 } ( y , z ) = _ { \mathrm { d e f } } \ \gamma _ { \varepsilon _ { v } } ( z )$ . This specifies δ, and we now calculate 

$$
\begin{array}{r l} \delta (f x, z) & = (\delta_ {1} (f x, z), \delta_ {2} (f x, z)) \\ & = (\varepsilon_ {f x}, \gamma_ {\varepsilon_ {f x}} (z)) \\ & = (1 _ {f x}, \gamma_ {1 _ {f x}} (z)) \\ & = (1 _ {f x}, 1 _ {z}) \\ & = 1 _ {(f x, z)} \end{array}
$$

as required. <sup></sup> 

For our second application of Lemma 13, let us recall that the category Gpd of small groupoids and functors admits a Quillen model structure $( \mathcal { W } , \mathcal { C } , \mathcal { F } )$ , in which the class of weak equivalences W consists of the categorical equivalences, the class of fibrations $\mathcal { F }$ consists of the Grothendieck fibrations, and the class of cofibrations $\mathcal { C }$ consists of the functors that are injective on objects [1,17]. As a consequence of this, both $( \boldsymbol { \mathfrak { W } } \cap \mathcal { C } , \mathcal { F } )$ and $( { \mathcal { C } } , { \mathcal { W } } \cap { \mathcal { F } } )$ are weak factorisation systems on Gpd. We shall be interested in relating the weak factorisation system $( \boldsymbol { \mathfrak { W } } \cap \mathcal { C } , \mathcal { F } )$ on Gpd with the identity type weak factorisation system on C(<sup>T</sup>). Let us recall that a functor $f : A $ B between groupoids is a Grothendieck fibration if and only if for every $\beta : f ( a )  b$ in B there exists α $: : a  a ^ { \prime }$ in A such that $f ( a ^ { \prime } ) = b { \mathrm { ~ a n d } } f ( \alpha ) = \beta$ . The required factorisation of a functor $f : A  B$ as an equivalence injective on objects followed by a Grothendieck fibration can be obtained using the familiar mapping space construction, 

$$
A \xrightarrow {i _ {f}} \operatorname{Path} (f) \xrightarrow {p _ {f}} B,
$$

where Path(f ) is the groupoid whose objects consist of triples $( a , b , \beta )$ , where $a \in A , b \in B ,$ , and $\beta : f ( a )  b$ in B. 

Theorem 15. Let $f : \phi  \psi$ be a context morphism. 

(i) $I f f \in { \mathcal { A } } ,$ , then $\mathcal { F } ( \phi )  \mathcal { F } ( \psi )$ is an equivalence injective on objects. 

(ii) $I f f \in { \mathcal { B } } $ , then $\mathcal { F } ( \phi )  \mathcal { F } ( \psi )$ is a Grothendieck fibration. 

Proof. For part (i), let $f : \phi  \psi$ be in A. By Lemma 13, f is a type-theoretic injective equivalence, so let us assume 

$$
(y \in \Psi) s (y) \in \Phi
$$

and the judgements in (20)–(22). We show that $\mathcal { F } ( s ) : \mathcal { F } ( \psi )  \mathcal { F } ( \phi )$ provides a quasi-inverse to $\mathcal { F } ( f ) : \mathcal { F } ( \phi )  \mathcal { F } ( \psi )$ First of all, we have a natural isomorphism $\mathcal { F } ( s ) \circ \mathcal { F } ( f ) \Rightarrow 1 _ { \mathcal { F } ( \psi ) }$ with components given by the maps $[ \varepsilon _ { b } ] : f ( s ( b ) ) \to b$ To establish naturality, we need to show that for every $q \in \mathrm { I d } ( b _ { 0 } , b _ { 1 } )$ ), there is a homotopy between $q \circ \varepsilon _ { b _ { 0 } }$ and $\varepsilon _ { b _ { 1 } } \circ f s ( q )$ which can be proved by elimination on $q \in \operatorname { I d } ( b _ { 0 } , b _ { 1 } )$ . Secondly, we have 

$$
\mathcal {F} (s) \circ \mathcal {F} (f) = \mathcal {F} (s \circ f) = \mathcal {F} (1 _ {\phi}) = 1 _ {\mathcal {F} (\phi)},
$$

which also shows that $\mathcal { F } ( f )$ is injective on objects, as required. For part (ii), let $f : \phi  \psi$ be a type-theoretic norma isofibration, and assume to have 

$$
(x \in \Phi , y \in \Psi , u \in \operatorname{Id} (f x, y)) j (x, y, u) \in \Phi
$$

and judgements as in (23) and (24). By (23), the map $) j : \operatorname { I d } ( f )  { \mathcal { P } }$ makes the following diagram commute 

$$
\begin{array}{c} \operatorname{Id} (f) \xrightarrow {j} \Phi \\ \Biggl \downarrow_ {p _ {f}} \Biggl \downarrow_ {f}. \\ \Psi \end{array}\tag{26}
$$

To prove that $\mathcal { F } ( f ) : \mathcal { F } ( \phi )  \mathcal { F } ( \psi )$ is a Grothendieck fibration, we will need an auxiliary result. We claim that there is a term 

$$
\left(x \in \Phi , y \in \Psi , u \in \operatorname{Id} (f x, y)\right) m (x, y, u) \in \operatorname{Id} _ {\operatorname{Id} (f)} \left(\left(x, f x, 1 _ {f x}\right), (x, y, u)\right).\tag{27}
$$

To see this, let us write $\Omega ( x , y , u ) = _ { \mathrm { d e f } } \mathrm { I d } _ { \mathrm { I d } ( f ) } { \big ( } ( x , f x , 1 _ { f x } ) , ( x , y , u ) { \big ) }$ . Then we have a commutative square 

$$
\begin{array}{c} \Phi \xrightarrow {k} (\operatorname{Id} (f), \Omega) \\ \Biggl \downarrow_ {i f} \qquad \qquad \qquad \qquad \qquad \qquad \qquad \Biggl \downarrow_ {p} \\ \operatorname{Id} (f) = \operatorname{Id} (f) \end{array}
$$

where k is given by $k = _ { \mathrm { d e f } } \ ( x , f x , 1 _ { f x } , 1 _ { ( x , f x , 1 _ { f } x ) } )$ , and p is the evident dependent projection. Because $i _ { f } \in \mathcal A$ and $p \in { \mathcal { B } }$ , we have by Weak Orthogonality a diagonal filler m: $\operatorname { I d } ( f )  ( \operatorname { I d } ( f ) , \varOmega )$ , as required for (27). 

We now show that $\mathcal { F } ( f )$ is a Grothendieck fibration. Let us consider a map $\beta : f ( a )  b$ in ${ \mathcal { F } } ( \psi )$ . Let $p \in { \mathrm { I d } } ( f ( a ) , b )$ be such that $\beta ~ = ~ [ p ]$ . Note that such a p exists, but it is neither unique nor determined canonically. We then define $a ^ { \prime } = _ { \mathrm { d e f } } j ( a , b , p )$ ). Next, we need to define $\alpha : a  a ^ { \prime }$ in $\mathcal { F } ( \phi )$ ). By (27), we have a term 

$$
m (a, b, p) \in \operatorname{Id} \bigl ((a, f a, 1 _ {f a}), (a, b, p) \bigr).
$$

We define a map $\theta : ( a , f a , 1 _ { f a } )  ( a , b , p )$ in $\mathcal { F } ( \operatorname { I d } ( f ) )$ by letting $\theta = [ m ( a , b , p ) ]$ ]. The required map $\alpha : a  a ^ { \prime }$ can then be defined as the result of an application of the functor $\mathcal { F } ( j )$ to θ. This has the required domain and codomain, since $a = j ( a , f ( a ) , 1 _ { f ( a ) } ) \in \phi$ by (24), and $a ^ { \prime } = j ( a , b , p ) \in \phi$ by the definition set earlier. Furthermore, the commutativity of the diagram in (26) implies that the result of applying $\mathcal { F } ( f )$ to α is $\beta ,$ as required. <sup></sup> 

We can now compare the factorisations in C(<sup>T</sup>) and in Gpd. 

Proposition 16. For every context morphism $f : \phi  \psi$ , we can define an equivalence surjective on objects σ<sub>f</sub> : $\mathcal { F } ( \mathrm { I d } ( f ) ) $ $\operatorname { P a t h } ( \mathcal { F } ( f ) )$ making the following diagram commute 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/68ea81b4-fda0-409c-8373-afc531902373/1f8d869b03c6fb2ae881e002aca0f3492544326e75ec052fd49e9f84344e0eb9.jpg)


Proof. The objects of $\mathcal { F } ( \operatorname { I d } ( f ) )$ are triples $( a , b , p )$ , where $p \in { \mathrm { I d } } ( f ( a ) , b )$ . The objects of $\operatorname { P a t h } ( \mathcal { F } ( f ) )$ are triples $( a , b , \alpha )$ where α is an arrow $\alpha : f ( a )  b$ in ${ \mathcal { F } } ( \phi )$ . Thus, $\sigma _ { f }$ can be defined as mapping $( a , b , p ) \ : \mathrm { t o } \ : ( a , b , [ p ] )$ . Direct calculations show the required properties. <sup></sup> 

Let us write J for the groupoid with two objects and an isomorphism between them. As a special case of Proposition 16, we obtain that for every context Φ, there is a surjective equivalence 

$$
\sigma : \mathcal {F} (x \in \varPhi , y \in \varPhi , u \in \operatorname{Id} (x, y)) \to \mathcal {F} (x \in \varPhi) ^ {\mathbf {J}},
$$

where $\mathcal { F } ( x \in \phi ) ^ { \mathbf { J } }$ can be seen as the groupoid of isomorphisms in $\mathcal { F } ( x \in \varPhi )$ . 

## Acknowledgements

We are grateful to Michael Warren for suggesting to use display maps rather than dependent projections in the definition of the identity type weak factorisation system, thus simplifying our original definition. We would also like to thank the referees for their useful comments. The research described here was started during a visit of the first-named author to the Department of Mathematics of the University of Uppsala and discussed further during the workshop Categorical and Homotopical Structures in Proof Theory, held at the Centre de Recerca Matemàtica. We gratefully acknowledge the support of both institutions. The second-named author is supported by a Research Fellowship of St John’s College, Cambridge, and a Marie-Curie Intra-European Fellowship, Project no. 040802. The use of Paul Taylor’s prooftree package is also acknowledged 

## Appendix. Structural rules for dependent type theories

## Axiom, weakening and substitution

The rule (∗) has the side-condition that the variable x should not appear as a free variable in Γ or ∆. When stating the rules below, J stands for an arbitrary judgement. 

$$
\frac {}{(\Gamma , x \in A)   x \in A} \quad \frac {(\Gamma , \Delta)   \mathcal {J} \quad (\Gamma)   A \in \text { Type }}{(\Gamma , x \in A , \Delta)   \mathcal {J}} (*) \quad \frac {(\Gamma , x \in A , \Delta)   \mathcal {J} \quad (\Gamma)   a \in A}{(\Gamma , \Delta [ a / x ])   \mathcal {J} [ a / x ]}.
$$

Reflexivity, symmetry, and transitivity of definitional equality of types 

$$
\frac {A \in \text { Type }}{A = A} \qquad \frac {A = B}{B = A} \qquad \frac {A = B \quad B = C}{A = C}.
$$

Reflexivity, symmetry, and transitivity of definitional equality of objects 

$$
\frac {a \in A}{a = a \in A} \qquad \frac {a = b \in A}{b = a \in A} \qquad \frac {a = b \in A \quad b = c \in A}{a = c \in A}.
$$

Compatibility rules for definitional equality 

$$
\frac {a \in A \quad A = B}{a \in B} \qquad \frac {a = b \in A \quad A = B}{a = b \in B}.
$$

## References



[1] D.W. Anderson, Fibrations and geometric realizations, Bulletin of the American Mathematical Society 84 (5) (1978) 765–788. 





[2] S. Awodey, M.A. Warren, Homotopy theoretic models of identity types, Mathematical Proceedings of the Cambridge Philosophical Society (in press). 





[3] R. Blackwell, G.M. Kelly, A.J. Power, Two-dimensional monad theory, Journal of Pure and Applied Algebra 59 (1989) 1–41. 





[4] A.K. Bousfield, Constructions of factorisation systems in categories, Journal of Pure and Applied Algebra 9 (1977) 207–220. 





[5] J. Cartmell, Generalised algebraic theories and contextual categories, Annals of Pure and Applied Logic 32 (1986) 209–243. 





[6] N.G. de Brujin, Telescopic mappings in typed lambda calculus, Information and Computation 91 (2) (1991) 189–204. 





[7] P. Dybjer, Internal type theory, in: S. Berardi, M. Coppo (Eds.), Types for Proofs and Programs, in: Lecture Notes in Computer Science, vol. 1158, Springer, 1997, pp. 120–134. 





[8] R. Garner, Two-dimensional models of type theory, 2008 (submitted for publication), ArXiv:0808.2122. 





[9] M. Hofmann, On the interpretation of type theory of locally Cartesian closed categories, in: L. Pacholski, J. Tiuryn (Eds.), Computer Science Logic 1994, in: Lecture Notes in Computer Science, vol. 933, Springer, 1995, pp. 427–441. 





[10] M. Hofmann, Syntax and semantics of dependent type theories, in: P. Dybjer, A.M. Pitts (Eds.), Semantics of Logics of Computation, Cambridge University Press, 1997, pp. 79–130. 





[11] M. Hofmann, Extensional Concepts in Intensional Type Theory, Springer, 1999. 





[12] M. Hofmann, T. Streicher, The groupoid model of type theory, in: G. Sambin, J. Smith (Eds.), Twenty-five Years of Constructive Type Theory, in: Oxford Logic Guides, vol. 36, Oxford University Press, 1998, pp. 83–111. 





[13] M. Hovey, Model categories, in: Mathematical Surveys and Monographs, vol. 63, American Mathematical Society, 1999. 





[14] W.A. Howard, The formulae-as-types notion of construction, in: J.R. Hindley, J.P. Seldin (Eds.), H. B. Curry: Essays in Combinatory Logic, Lambda Calculus, and Formalism, Academic Press, 1980, pp. 479–490. 





[15] B. Jacobs, Categorical logic and type theory, in: Studies in Logic and the Foundations of Mathematics, vol. 141, Elsevier, 1999. 





[16] A. Joyal, The theory of quasi-categories and its applications, Quaderns 45, Centre de Recerca Matemàtica, 2008. 





[17] A. Joyal, M. Tierney, Strong stacks and classifying spaces, in: Category Theory (Como 1990) (Berlin), in: Lecture Notes in Mathematics, vol. 1488, Springer, 1991, pp. 213–236. 





[18] S. Lack, Homotopy—theoretic aspects of 2-monads, Journal of Homotopy and Related Structures 2 (2) (2007) 229–260. 





[19] J. Lambek, P.J. Scott, Introduction to higher-order categorical logic, in: Cambridge Studies in Advanced Mathematics, vol. 7, Cambridge University Press, 1986. 





[20] F.W. Lawvere, Functorial semantics, Proceedings of the National Academy of Sciences of the United States of America 50 (1963) 869–872 





[21] M.E. Maietti, Modular correspondence between dependent type theories and categorical universes including pretopoi and topoi, Mathematica Structures in Computer Science 15 (6) (2005) 1089–1149. 





[22] P. Martin-Löf, Intuitionistic type theory — Notes by Giovanni Sambin of a series of lectures given in Padua, June 1980, Blibliopolis, 1984. 





[23] J.P. May, A concise course in algebraic topology, in: Chicago Lecture Notes in Mathematics, The University of Chicago Press, 1999. 





[24] B. Nordström, K. Petersson, J.M. Smith, Programming in Martin-Löf type Theory: An Introduction, Oxford University Press, 1990. 





[25] B. Nordström, K. Petersson, J.M. Smith, in: S. Abramsky, D.M. Gabbay, T.S.E. Maibaum (Eds.), Martin-Löf Type Theory, in: Handbook of Logic in Computer Science. Volume V, Oxford University Press, 2001, pp. 1–37. 





[26] A.M. Pitts, Categorical logic, in: S. Abramsky, D.M. Gabbay, T.S.E. Maibaum (Eds.), Handbook of Logic in Computer Science. Volume V, Oxford University Press, 2001, pp. 39–128. 





[27] J. Rosický, W. Tholen, Lax factorisation algebras, Journal of Pure and Applied Algebra 175 (3) (2002) 335–382. 





[28] D.S. Scott, Constructive validity, in: Symposium on Automated Demonstration, in: Lecture Notes in Mathematics, vol. 125, Springer, 1970, pp. 237–275. 





[29] D.S. Scott, Relating theories of the λ-calculus, in: J.R. Hindley, J.P. Seldin (Eds.), H. B. Curry: Essays in Combinatory Logic, Lambda Calculus, and Formalism, Academic Press, 1980, pp. 403–450. 





[30] R.A.G. Seely, Locally Cartesian closed categories and type theories, Mathematical Proceedings of the Cambridge Philosophical Society 95 (1984) 33-48 





[31] R. Street, Fibrations and Yoneda’s lemma in a 2-category, in: G.M. Kelly, R.H. Street (Eds.), Category Seminar (Proc. Sem. Sydney 1972/73), in: Lecture Notes in Mathematics, vol. 420, Springer, 1974, pp. 104–133. 





[32] T. Streicher, Investigations into intensional type theory, Habilitationsschrift, Ludwig-Maximilians Universität München, 1993. 





[33] P. Taylor, Practical foundations of mathematics, in: Cambridge Studies in Advanced Mathematics, vol. 59, Cambridge University Press, 1999. 

