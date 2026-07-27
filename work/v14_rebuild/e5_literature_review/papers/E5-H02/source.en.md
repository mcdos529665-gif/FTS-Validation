# Representable Markov Categories and Comparison of Statistical Experiments in Categorical Probability

Tobias Fritz<sup>∗1</sup>, Tom´aˇs Gonda<sup>†2,3</sup>, Paolo Perrone<sup>‡4</sup>, and Eigil Fjeldgren Rischel<sup>§5</sup> 

<sup>1</sup>Department of Mathematics, University of Innsbruck, Austria <sup>2</sup>Perimeter Institute for Theoretical Physics, Waterloo ON, Canada <sup>3</sup>School of Physics and Astronomy, University of Waterloo, Canada <sup>4</sup>Massachusetts Institute of Technology, Cambridge MA, U.S.A. <sup>5</sup>University of Strathclyde, Glasgow, Scotland 

December 22, 2024 

## Abstract

Markov categories are a recent categorical approach to the mathematical foundations of probability and statistics. Here, this approach is advanced by stating and proving equivalent conditions for second-order stochastic dominance, a widely used way of comparing probability distributions by their spread. Furthermore, we lay the foundation for the theory of comparing statistical experiments within Markov categories by stating and proving the classical Blackwell–Sherman–Stein Theorem. Our version not only ofers new insight into the proof, but its abstract nature also makes the result more general, automatically specializing to the standard Blackwell–Sherman–Stein Theorem in measure-theoretic probability as well as a Bayesian version that involves prior-dependent garbling. Along the way, we define and characterize representable Markov categories, within which one can talk about Markov kernels to or from spaces of distributions. We do so by exploring the relation between Markov categories and Kleisli categories of probability monads. 

Keywords—Categorical probability; Markov category; Kleisli category; Blackwell–Sherman–Stein Theorem; Second-order stochastic dominance; Comparison of statistical experiments 

## Contents

1 Introduction 2   
2 Markov Categories 7   
2.1 Definition of Markov Categories and Basic Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   
3 Representable Markov Categories 12   
3.1 Kleisli Categories as Markov Categories. 12   
3.2 Markov Categories as Kleisli Categories. 18   
3.3 Almost-Surely-Compatible Representability. 26   
4 Second-Order Stochastic Dominance 30   
5 Comparison of Statistical Experiments 35   
5.1 Informativeness of Statistical Experiments. 35   
5.2 The Classical Blackwell-Sherman-Stein Theorem. 41   
5.3 The Blackwell-Sherman-Stein Theorem in Markov Categories. 43   
5.4 The Blackwell-Sherman-Stein Theorem Parametrized by Priors. 50   
6 Strongly Representable Markov Categories 58 

## 1 Introduction

Traditionally, the foundations of mathematical statistics are rooted in measure theory and measure-theoretic probability. More generally, mathematical statistics and probability theory are typically considered as mathematical subjects of a clearly analytical nature. While this has worked well in practice, it is also often the case in mathematics that higher abstraction leads ultimately to deeper understanding, greater generality and ultimately facilitates the development of results and methods of greater complexity. 

This is what the growing field of categorical probability attempts to do by developing a category-theoretical foundation for probability theory and mathematical statistics. A promising approach is provided by Markov categories which, in line with categorical thinking, focuses on the morphisms involved in probabilistic reasoning, namely stochastic maps (or Markov kernels). There is growing evidence that Markov categories can serve both as a categorical foundation for, as well as a generalization of, ordinary measure-theoretic probability theory. Indeed, similar to how a computer can be programmed either in terms of low-level machine code or in a more accessible and hardware-independent abstract language, it seems to be the case that probability theory likewise can be practiced either in concrete analytical terms based on Kolmogorov’s axioms, or in a more abstract synthetic form based on the structural axioms of Markov categories. 

More specifically, Markov categories allow one to study and make use of: 

• Bayes’ theorem and Bayesian updating: This was first considered by Golubtsov in [17] and rediscovered recently by Cho and Jacobs [9], with further results on the dagger functor structure of Bayesian inversion in the first named author’s [12]. 

• Conditional independence: This was also defined within this framework by Cho and Jacobs [9], and more generally in [12, Section 12]. 

• Almost sure equality: Again, first done by Cho and Jacobs [9] and then generalized and developed further in [12, Section 13]. 

• Suficient statistics: Some of the basic theorems on suficient statistics were proven abstractly in [12, Sections 14–16]. 

• Kolmogorov extension theorem and 0/1-laws: The Kolmogorov products developed by the first-named and last-named author, which arise as infinite products in Markov categories formalizing the Kolmogorov extension theorem, have facilitated synthetic proofs of the classical 0/1-laws of Kolmogorov and Hewitt–Savage [15]. 

• Patterson has developed an algebraic approach to statistical models, drawing and exploiting relations to categorical logic [24]. 

Of course, this only lists those aspects of probability theory and statistics which have been developed synthetically up to the present time and to our knowledge. The present paper has two goals: first, to continue the development of the general categorical theory; and second, to add two more items to the above list, namely second-order stochastic dominance and the classical Blackwell–Sherman– Stein Theorem on the comparison of statistical experiments. We now summarize our results on both of these goals, which are related through the latter applications drawing on the former categorical developments. 

Outline and results. In practice, Markov categories often arise as Kleisli categories of afine symmetric monoidal monads. For example, this is the case for BorelStoch, the category of standard Borel spaces and measurable Markov kernels, or equivalently the Kleisli category of the Giry monad on the category of standard 

Borel spaces and measurable maps. In Section 3, we clarify the relation between Markov categories and Kleisli categories of this type, namely Kleisli categories of afine symmetric monoidal monads on categories with finite products. We find that for a Markov category C, the question of whether C arises as a Kleisli category like this is closely linked to the existence of a right adjoint to the inclusion functor $\mathsf C _ { \mathrm { d e t } } \hookrightarrow \mathsf C ,$ where $\mathsf { C } _ { \mathrm { d e t } }$ is the cartesian monoidal subcategory of deterministic morphisms in C; for if C is supposed to be the Kleisli category of a monad on $\mathsf { C } _ { \mathrm { d e t } }$ , then this right adjoint must exist for purely formal reasons. The existence of such $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ amounts to the natural bijection 

$$
\mathsf {C} _ {\mathrm{det}} (A, P X) \cong \mathsf {C} (A, X),\tag{1.1}
$$

which we interpret as the existence of a distribution functor that, for $A = I$ , identifies the deterministic morphisms $I  P X$ with the “distributions” over X (morphisms $I  X )$ . More generally, (not necessarily deterministic) morphisms $A  X$ can be thought of as being “classified” by deterministic morphisms $A  P X$ . Not every Markov category has such a distribution functor. For example, the category of finite sets and stochastic matrices FinStoch does not, since FinStoch $( A , X )$ is generically infinite, while instead its putative counterpart $\mathsf { F i n S t o c h \mathrm { { d e t } } } ( A , P X )$ would necessarily have to be finite. 

Our results on the connection between Markov categories and Kleisli categories are then as follows: 

• We prove that if P is an afine symmetric monoidal monad on a cartesian monoidal category D, and P satisfies a certain pullback condition, then the Kleisli category $\mathsf { K I } ( P )$ is a Markov category such that the subcategory of deterministic morphisms ${ \sf K I } ( P ) _ { \mathrm { d e t } }$ is exactly the original category D. 

• Conversely, if a Markov category C has a distribution functor P , meaning a right adjoint for the inclusion $\mathsf C _ { \mathrm { d e t } } \hookrightarrow \mathsf C$ , then the induced monad on $\mathsf { C } _ { \mathrm { d e t } }$ satisfies the pullback condition, and C is isomorphic to the Kleisli category of P (Theorem 3.16). 

We end Section 3 by studying the interaction between the distribution functor P and the notion of almost sure equality in C. If these are compatible in a suitable sense, then we say that C is a.s.-compatibly representable. Distribution functors and a.s.-compatible representability will then play a central role in the subsequent two sections that focus on applications of the general theory. 

In Section 4, we provide a categorical description and generalization of secondorder stochastic dominance, which is a way of comparing probability distributions with respect to how “spread out” they are. This notion also appears in Blackwell– Sherman–Stein (BSS) theorem, a classical and widely used fundamental result that connects it to the question of comparing statistical experiments in terms of their informativeness about the tested hypotheses. 

In Section 5, we introduce the informativeness preorder in Markov categories, and prove Theorem 5.4 that characterizes it in terms of the notions of suficient statistics and conditional independence. Most of this section, however, is devoted to a categorical version of the BSS theorem. In fact, we have a few variations thereof. The closest to the standard version that concerns a discrete parameter space is Corollary 5.15, but it more generally applies to any a.s.-compatibly representable Markov category other than BorelStoch. In our presentation, this result arises as a corollary of Theorem 5.13 for more general parameter spaces, which considers a fixed prior distribution and compares experiments with respect to whether they are “almost surely more informative”. Concretely, in the context of standard Borel spaces, Theorem 5.13 says the following. 

Theorem. Let X, Y and Θ be standard Borel spaces, and let $( f _ { \theta } ) _ { \theta \in \Theta }$ and $( g _ { \boldsymbol { \theta } } ) _ { \boldsymbol { \theta } \in \Theta }$ be families of probability measures on X and Y respectively, parametrized measurably in θ. Let m be a probability measure on Θ. Then the following are equivalent: 

1. There is a Markov kernel c: $X  Y$ such that $g _ { \theta } = c f _ { \theta }$ holds for m-almost all θ. 

2. The standard measures $\hat { f } _ { m }$ and $\hat { g } _ { m }$ (probability measures on P Θ—the space of probability measures) are such that $\hat { g } _ { m }$ second-order dominates $\hat { f } _ { m }$ 

In this formulation of the BSS Theorem, we do not need to assume that the parameter space Θ be finite or even countable. 

We then present a completely prior-independent version of the BSS theorem in Section 5.4. This result avoids the need for a prior by efectively considering all priors at once. In our categorical formulation, it turns out to be a special case of the earlier Theorem 5.13; but when instantiated in BorelStoch, we obtain the following statement. 

Theorem. Let X, Y and Θ be standard Borel spaces, and let $( f _ { \theta } ) _ { \theta \in \Theta }$ and $( g _ { \boldsymbol { \theta } } ) _ { \boldsymbol { \theta } \in \Theta }$ be families of probability measures on X and Y respectively, parametrized measurably in θ. Then the following are equivalent: 

1. There is a family of Markov kernels $( c _ { m } \colon X \to Y ) _ { m \in P \Theta }$ , depending measurably on the prior m, such that $g _ { \theta } = c f _ { \theta }$ holds for m-almost all θ and all $m \in P \Theta$ 

2. The standard measures $\hat { f } _ { m }$ and $\hat { g } _ { m }$ are such that $\hat { g } _ { m }$ second-order dominates $\hat { f } _ { m } ~ f o r$ every choice of prior m $\in ~ { \cal P } \Theta$ , as witnessed by a family of dilations $( t _ { m } ) _ { m \in P ^ { \ominus } }$ that depend measurably on m. 

Moreover, as we show in Proposition 5.19, these conditions are not in general equivalent to f being more informative than g with respect to a prior-independent garbling map. 

Finally, in Section 6, we consider a notion that we call strong representability. This is a further strengthening of the notion of a.s.-compatible representability for Markov categories, which may be more natural in some situations. Instead of requiring compatibility with the relation of almost sure equality, it asks for compatibility with the formation of conditionals—specifically, with the notion of conditional determinism. 

Outlook. Given the relevance of the theory of comparison of experiments in a wide array of situations, such as hypothesis testing or error correction, proving versions of celebrated results—such as the BSS Theorem—in the abstract context of Markov categories leads to a greater level of generality which has the potential for new domains of applications. The understanding of these results in a synthetic way also has the potential to overcome some of the limitations of the standard approaches, such as the discreteness of the parameter spaces involved. 

With the recent development of quantum Markov categories [23], it is conceivable that one could obtain a synthetic version of the quantum BSS Theorem [7] and related results, with potential applications to quantum hypothesis testing or quantum error correction. 

Finally, the categorical approach also lends itself to the considerations of variants of the theory in which additional restrictions are placed on the garbling maps. For example, such variations can be studied under the hood of resource theories of distinguishability as introduced in [18, Appendix C]. Many interesting restrictions arise from requiring equivariance of the garbling maps with respect to group actions. Others include adaptive garbling maps or garbling via independent action of multiple agents, both of which are considered in [11]. Although we have not done this yet, it should be straightforward to instantiate Theorem 5.13 and Corollary 5.20 in suitable categories, so as to obtain measure-theoretic BSS theorems which apply in such contexts. 

Acknowledgments. We thank Robert Furber for helpful feedback on measuretheoretic aspects as well as Luciano Pomatto for helpful feedback on a draft. Research for the third author is funded by AFOSR grants FA9550-19-1-0113 and FA9550-17- 1-0058. Research for the second author is supported by NSERC Discovery grant RGPIN 2017-04383, and by the Perimeter Institute for Theoretical Physics. Research at Perimeter Institute is supported in part by the Government of Canada through the Department of Innovation, Science and Economic Development Canada and by the Province of Ontario through the Ministry of Colleges and Universities. 

## 2 Markov Categories

## 2.1 Definition of Markov Categories and Basic Theory

We now recall the definition of Markov category. As far as we know, it was first proposed by Golubtsov as category of information transformers in slightly diferent form [17], and rediscovered recently by Cho and Jacobs as afine CD-categories [9]. The simpler term Markov category was subsequently coined in [12], based on the idea that Markov categories are abstract generalizations of the category of Markov kernels. 

Definition 2.1. A Markov category C is a semicartesian symmetric monoidal category where every object $X \in \mathsf C$ is equipped with a distinguished morphism 

$$
\operatorname{copy} _ {X} = \bigcup_ {X} ^ {X} \begin{array}{c c} X & X \\ \hline \end{array}\tag{2.1}
$$

which, together with the unique morphism del $x \colon X \to I$ , makes X into a commutative comonoid, and such that 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/24c5c43ff6ff53feb73dd6d1953fce663a3310d1e489f5e9d56fdd99e93a2be4.jpg)


(2.2) 

for all X, $Y \in \mathsf { C }$ 

Throughout this manuscript, C denotes a Markov category. 

Among the prototypical examples of a Markov category is BorelStoch, the category of standard Borel spaces and measurable Markov kernels. A more basic example is FinStoch, the category of finite sets and stochastic matrices. In both cases, the comultiplications copy $\mathbf { \Phi } _ { X } \colon X \to X \otimes X$ are given by the diagonals $x \mapsto \delta _ { ( x , x ) } .$ assigning to every element $x \in X$ the Dirac delta distribution $\delta _ { ( x , x ) } ;$ this is the stochastic way to talk about copying. Markov categories can also be obtained from categories of relations, such as Rel, by restricting to relations $R \colon X \not \sim Y$ which have the property that for every $x \in X$ there is $y \in Y$ with xRy; this is the relational analogue of the normalization of probability. This results in a Markov category with respect to the usual cartesian product as monoidal structure, and the copy maps are again given by the obvious diagonals. Another interesting class of examples arises by noting that diagram categories of Markov categories are again Markov categories (when suitably defined [12, Section 7]), and we expect that this can be used as a basis for a synthetic theory of stochastic processes. 

Definition 2.2. A morphism $f \colon X \to Y$ in C is deterministic if it respects the copy maps: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/f9b2b5ca1028867ecd17f2e97d80a4cac1bcd716b3497897c4b92a48eadd836b.jpg)


(2.3) 


The subcategory of C that consists of its deterministic morphisms is denoted by $\mathsf { C } _ { \mathrm { d e t } }$


This type of condition goes back to the seminal paper of Carboni and Walters on cartesian bicategories [8]. Intuitively, it means that applying f to two independent copies of its input is guaranteed to result in the same pair of output values than applying f directly to the input and copying its output. C is a cartesian monoidal category with respect to the monoidal structure inherited from $\mathsf { C } ,$ and all structure morphisms of C, including the copy maps, are in $\mathsf { C } _ { \mathrm { d e t } }$ [12, Remark 10.13]. 

Other key notions within Markov categories that we use in Sections 4 and 5 include conditionals, Bayesian inverses, almost sure equality, and domination (in the sense of absolute continuity). All but the last of these notions have been introduced in earlier works [9, 12]. We now recall their definitions. 

Definition 2.3. Given $f \colon A \to X \otimes Y$ in C, a morphism $f _ { | X } \colon X \otimes A \to Y$ in C is 

called a conditional of f with respect to X if the equation 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/bff742e13b1fc4be557a59b10c05cb7de09575f0d2ad0a99503f526dcd7eded8.jpg)


(2.4) 

holds. We say that C has conditionals provided that such a conditional exists for all objects $A , X , Y \in { \mathsf { C } }$ and all $f \colon A \to X \otimes Y$ in C. 

We can also consider conditionals of $f \colon A \to X \otimes Y$ with respect to $Y$ , which are defined in the analogous way. Using the symmetry of C shows that these automatically exist if C has conditionals. 

Example 2.4. BorelStoch has conditionals [12, Example 11.7]. As far as we know at the moment, the earliest reference for this measure-theoretic fact is in Kallenberg’s textbook on random measures [19, Theorem 1.25]. 

Definition 2.5. Given two morphisms m: $I \ \to \ A$ and $f \colon A \ \to \ X$ , a Bayesian inverse $o f f$ with respect to (the prior) m is a conditional of 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/d5b76424cc7f6d230307094bbe4f8d339bf71f2e08b38fe31b529fcf618894dc.jpg)


(2.5) 

with respect to $X$ . 

The choice of a prior is often clear from context, so we denote a Bayesian inverse of $f$ simply by $f ^ { \dagger } \colon X \to A$ with the dependence on m left implicit. Thus a Bayesian inverse $f ^ { \dagger }$ is defined to be a morphism satisfying the equation: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7f8fe6f51b5381bc4765a1c1e0acec57756c1d5de072afbf6a2b55299d5cd1d4.jpg)


(2.6) 

Even though conditionals and Bayesian inverses are generally not unique when they exist, it is clear from the definition that they are unique up to almost sure equality [12, Proposition 13.6], which in general is defined as follows. 

Definition 2.6. Given any morphism h: $A \ \to \ X ,$ , we say that any two parallel $f , g \colon X \to Y$ are h-almost surely equal, denoted by $f = _ { h - a . s . ~ { \it g } }$ , if we have 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/669b01a0fc2dd19599e84cd8e77ac38af9d93cfff4d3d45eb34eed94dfe3eb44.jpg)


(2.7) 

Example 2.7. In the context of BorelStoch, Definition 2.6 recovers the expected notion of equality almost surely as has been shown in [9, Proposition 5.4]. In particular, given Markov kernels $f , g \colon X \to Y$ and $\nu \colon I \to X$ , the relation $f = \scriptstyle \nu \dotsc s . \ g$ means exactly that for all $S \in \Sigma _ { X }$ and $T \in \Sigma _ { Y }$ , we have 

$$
\int_ {S} f (T | x) \nu (d x) = \int_ {S} g (T | x) \nu (d x),\tag{2.8}
$$

or equivalently that the integrands $f ( T | _ { - } )$ and $g ( T | _ { - } )$ are ν-almost everywhere equal for all $T$ 

The following notion of measure domination is new in the context of Markov categories. 

Definition 2.8. Given two morphisms µ, $\nu \colon I \to X$ , we say that $\mu$ is dominated by $\nu ,$ denoted $\mu \ll \nu ,$ , if for all objects X and all morphisms $f , g \colon X \to Y$ we have 

$$
f = _ {\nu - a. s.} g \quad \Longrightarrow \quad f = _ {\mu - a. s.} g.\tag{2.9}
$$

Example 2.9. In BorelStoch, Definition 2.8 recovers the standard notion of domination of probability measures (also known as absolute continuity preorder), given by the condition that for all measurable sets $S \in \Sigma _ { X }$ , we must have 

$$
\nu (S) = 0 \quad \Longrightarrow \quad \mu (S) = 0.\tag{2.10}
$$

To prove that this is indeed the case, suppose first that condition (2.10) holds. One can then replace ν with $\mu$ in equation (2.8), so that $f = \scriptstyle \nu \dotsc s . g$ indeed implies $f = _ { \mu \mathrm { - } \mathrm { a . s . } } ~ g$ as necessary to conclude $\mu \ll \nu$ according to Definition 2.8. 

In the converse direction, suppose that $\mu \ll \nu$ holds in the sense of Definition 2.8, and that $\nu ( S ) = 0$ for some $S \in \Sigma _ { X }$ . Consider f and $g$ to be the Markov kernels associated to the measurable functions $1 _ { S } \colon X \to \{ 0 , 1 \}$ and $X  \{ 0 , 1 \} , \ x \mapsto 0$ respectively. Then we have $f = \scriptstyle \nu \dotsc s . \ g$ by $\nu ( S ) = 0$ . However, together with $\mu \ll \nu$ this gives $f = _ { \mu \mathrm { - } \mathrm { a . s . } } ~ g$ , which is just a diferent way to write $\mu ( S ) = 0$ given our choice of f and $g .$ . 

## 2.2 Parametric Markov Categories

In order to demonstrate the power of the synthetic treatment of the notions of secondorder stochastic dominance and comparison of statistical experiments later, we use the following new class of Markov categories throughout this paper. 

Given any Markov category C and any object $W \in \mathsf C$ , we now define a new Markov category ${ \mathsf { C } } _ { W }$ which we call the Markov category parametrized by $W$ , or simply a parametric Markov category when referring to no particular choice of $W$ The objects of ${ \mathsf { C } } _ { W }$ coincide with those of C, and its morphisms $A  X$ are defined to be precisely the morphisms $B \otimes A  X$ in C, that is 

$$
\mathsf {C} _ {W} (A, X) := \mathsf {C} (W \otimes A, X).\tag{2.11}
$$

We think of the object W as playing the role of a “parameter space” which indexes a family of morphisms $A  X$ . In order to distinguish notationally between morphisms $A  X$ in ${ \mathsf { C } } _ { W }$ and their representatives $W \otimes A \to X$ in C, we use blue colored text and diagrams whenever the former representation is used, but otherwise use the same symbol to denote the two. The composition of morphisms in ${ \mathsf { C } } _ { W }$ is defined by distributing the parameter in W via the copy map copy ${ \bf \dot { \boldsymbol { W } } } ^ { \flat } ( { \boldsymbol { W } } )$ 

$$
\begin{array}{c c} Y & = \\ \framebox {g} & \framebox {f} \\ A & W \end{array} \quad \begin{array}{c c} Y & \\ \framebox {g} & \\ \framebox {f} & \\ W & A \end{array}\tag{2.12}
$$

The tensor product of morphisms in ${ \mathsf { C } } _ { W }$ is likewise defined by supplying copies of W to the respective morphisms, 

$$
\begin{array}{c c} \boxed {X} & Y \\ \boxed {f} & \boxed {g} \\ A & B \end{array} = \quad \boxed { \begin{array}{c c} X & Y \\ \hline f & g \\ W & A \end{array} }\tag{2.13}
$$

and with the monoidal structure morphisms being precisely those of C itself. The discarding operation del<sub>X</sub> in ${ \mathsf { C } } _ { W }$ just consists of discarding both W and X. Finally, the copying in ${ \mathsf { C } } _ { W }$ also discards the parameter, 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/3262e017a3c39373154c0e53b9d44f1dca6b6784f5a1509e34166ca2da9d2451.jpg)


(2.14) 

It is then straightforward to verify that ${ \mathsf { C } } _ { W }$ is indeed also a Markov category. 

We can alternatively think of ${ \mathsf { C } } _ { W }$ as the co-Kleisli category of the reader comonad $W \otimes _ { - } \operatorname { o n } { \mathsf { C } }$ (see for example [25, Section 5.3]). Note that, while the reader comonad is usually defined on cartesian monoidal categories, the only property of cartesian monoidal categories that is actually used in the definition is that the object W has a comonoid structure, and thus this co-Kleisli category still makes sense in our context. 

Lemma 2.10. If C has conditionals, then so does every parametric Markov category ${ \mathsf { C } } _ { W }$ 

Proof. If $f \colon A \to X \otimes Y$ is a morphism in ${ \mathsf { C } } _ { W }$ represented by $f \colon W \otimes A \to X \otimes Y$ in $\mathsf { C } ,$ then every conditional $f _ { | X } \colon X \otimes W \otimes A \to Y$ of $f$ with respect to X represents a conditional $f _ { | X }$ of $f$ in ${ \mathsf { C } } _ { W }$ upon permuting its input factors to $W \otimes ( X \otimes A )$ □ 

## 3 Representable Markov Categories

## 3.1 Kleisli Categories as Markov Categories

It was argued by Kock [21] that afine commutative monads provide a convenient categorical framework for theories of distributions. The following result, which is a special case of [12, Proposition 3.1] gives one direction of the connection between this monadic approach and Markov categories. 

Recall first that a monad $P$ on a category with a terminal object 1 is called afine if $P ( 1 ) \cong 1$ ; and also that commutative monads and symmetric monoidal monads are equivalent concepts [6, Proposition 6.3.5], so that the following takes a variant of Kock’s framework as its starting point. 

Proposition 3.1. Let D be a cartesian monoidal category, and let $( P , E , \delta )$ be an afine symmetric monoidal monad on D with monoidal structure maps 

$$
\nabla \colon P (\_ \times P (\_ \longrightarrow P (\_ \times \_).\tag{3.1}
$$

Then the Kleisli category $\mathsf { K I } ( P )$ is a Markov category with respect to the following pieces of structure: 

• The monoidal structure on objects is given by products in D, and the monoidal product of Kleisli morphisms $f \colon A \to P X$ and $g \colon B \to P Y$ represented by the composite 

$$
A \times B \xrightarrow {f \times g} P X \times P Y \xrightarrow {\nabla} P (X \times Y),
$$

• The copy maps $\operatorname { c o p y } _ { X }$ are represented by the overall composite of the diagram 

$$
\begin{array}{c} X \xrightarrow {\delta} P X \\ (\mathrm{id,id}) \Big \downarrow \qquad \qquad \qquad \qquad \qquad \qquad \qquad \Big \downarrow (\mathrm{id,id}) \\ X \times X \xrightarrow {\delta \times \delta} P X \times P X \\ \Big \downarrow \qquad \qquad \qquad \qquad \Big \downarrow \nabla \\ P (X \times X) \end{array}\tag{3.2}
$$

Note that the upper square in equation (3.2) commutes trivially, while the lower triangle commutes as one of the defining properties of monoidal monads. 

Example 3.2. This construction reproduces BorelStoch as the Kleisli category of the Giry monad on the category of standard Borel spaces and measurable maps; the definition of the copy maps reproduces exactly the maps $x \mapsto \delta _ { ( x , x ) }$ described above. 

Example 3.3. Let $( R , + , \cdot , 0 , 1 )$ be a commutative semiring, i.e., a set R equipped with algebraic structure like that of a commutative ring except for the assumption of additive inverses. Then R induces an afine symmetric monoidal monad $D _ { R }$ on Set, given by the R-linear combinations monad together with a normalization constraint. This is spelled out, for example, in [10, Section 5.1], which we recall here. 

For each set X, denote by $D _ { R } X$ the set of functions p : $X  R$ which are nonzero on finitely many elements, and such that the normalization constraint 

$$
\sum_ {x \in X} p (x) = 1\tag{3.3}
$$

holds. This sum is well-defined thanks to the fact that it has at most a finite number of nonzero summands, which is also the case for all other sums appearing in this example. 

For every set function $f \colon X \to Y$ , we can construct the corresponding function $D _ { R } f \colon D _ { R } X \to D _ { R } Y$ as follows. Given $p \in D _ { R } X$ , we define $( D _ { R } f ) ( p )$ to be the map 

$$
y \mapsto \sum_ {x \in f ^ {- 1} (y)} p (x).\tag{3.4}
$$

This makes $D _ { R }$ into a functor. The unit of the monad has components η : $X \to D _ { R } X$ that map each $x \in X$ to $\eta ( \boldsymbol { x } ) \colon X \to R$ defined by 

$$
x ^ {\prime} \mapsto \left\{ \begin{array}{l l} 1 & \text { if } x = x ^ {\prime}, \\ 0 & \text { if } x \neq x ^ {\prime}, \end{array} \right.\tag{3.5}
$$

generalizing the Dirac delta distribution to the commutative semiring setting. The monad multiplication map $\mu \colon D _ { R } D _ { R } X \to D _ { R } X$ is given by 

$$
\mu (\phi) (x) := \sum_ {p \in D _ {R} X} \phi (p) \cdot p (x)\tag{3.6}
$$

for all $\phi \in D _ { R } D _ { R } X$ and $x \in X$ , where the product is taken in R. The monoidal unit map is uniquely determined because $D _ { R } I \cong I$ is the terminal object. Finally, the monoidal multiplication map ∇: $D _ { R } X \times D _ { R } Y  D _ { R } ( X \times Y )$ is given by 

$$
\nabla (p, q) (x, y) := p (x) \cdot p (y)\tag{3.7}
$$

for all $p \in D _ { R } ( X ) , q \in D _ { R } ( Y ) , x \in X$ and $y \in Y$ . The commutativity of R is relevant for showing that this lax monoidal structure is symmetric. We leave the detailed verifications to the reader. 

Hence we have specified $D _ { R }$ as an afine symmetric monoidal monad on Set, which we call the (generalized) distribution monad valued in R. By Proposition 3.1, its Kleisli category is canonically a Markov category. 

Returning to the general theory, we consider the relation between D and the subcategory of deterministic morphisms ${ \sf K I } ( P ) _ { \mathrm { d e t } }$ in the Kleisli category. Clearly, the canonical identity-on-objects functor $\mathsf {  ~ \mathsf { D } ~ } \to \mathsf {  ~ \mathsf { K I } } ( \boldsymbol { P } )$ lands in ${ \sf K I } ( P ) _ { \mathrm { d e t } }$ For particular monads P it often happens that this functor is fully faithful, and hence an isomorphism of categories: The original category D is precisely the category of deterministic morphisms. 

For example, this happens with the Giry monad on standard Borel spaces, for which the Kleisli category is BorelStoch [12, Example 10.5]. On the other hand, it does not happen for Stoch as the Kleisli category of the Giry monad on all measurable spaces: There are {0, 1}-valued probability measures on suitable measurable spaces $\left( X , \Sigma _ { X } \right)$ which are not delta measures [12, Example 10.4]. Some unfolding of the definitions shows that such a measure defines a deterministic morphism $I  ( X , \Sigma _ { X } )$ in Stoch which does not correspond a measurable map $I  ( X , \Sigma _ { X } )$ , since the latter correspond exactly to the delta measures on X. 

We now present a general criterion which guarantees that there are no such “accidental” deterministic morphisms. Intuitively, it states that the delta distributions should be precisely those distributions which are independent of themselves, or equivalently, that they should be the only product measures supported on the diagonal. 

Proposition 3.4. Let $( P , E , \delta )$ be an afine symmetric monoidal monad on a cartesian monoidal category D. Then the canonical functor $\mathsf { D } \to \mathsf { K I } ( P ) _ { \mathrm { d e t } }$ is an isomorphism of categories if and only if the diagram 

$$
\begin{array}{c} X \xrightarrow {\delta} P X \\ (\delta , \delta) \Biggl \downarrow \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \Biggl \downarrow P (\mathrm{id}, \mathrm{id}) \\ P X \times P X \xrightarrow {\nabla} P (X \times X) \end{array}\tag{3.8}
$$

is a pullback for every $X \in \mathsf { D }$ 

Proof. The monoidal structure map ∇ has a left inverse given by the canonical map 

$$
\Delta \colon P (X \times X) \to P X \times P X
$$

induced from the cartesian monoidal structure of D (note that this map corresponds to marginalization in the probability context [14]). Therefore, ∇ is a monomorphism. Since monomorphisms are stable under pullback, it follows that $\delta \colon X \to P X$ is a monomorphism as well. This implies that the canonical functor $\mathsf { D } \to \mathsf { K I } ( P ) _ { \mathrm { d e t } }$ is faithful. 

To prove fullness, let $f \colon A \to P X$ be the representative of a deterministic Kleisli morphism $A  X$ in the Markov category $\mathsf { K I } ( P )$ . Some unfolding of the definitions shows that the determinism assumption amounts exactly to commutativity of the diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/0044667981e4775dccd9716cdcf581c22b68b2538210610a22f41c7a2b2c70fd.jpg)


(3.9) 

But now the assumption that diagram (3.8) is a pullback lets us obtain the dashed arrow $\tilde { f }$ in 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/582f4a231f0e3f009c067a0321399e784c06efb843af83b35ad3161737f293ab.jpg)


(3.10) 

which is exactly the factorization of f needed to show that it is in the image of $\mathsf { D } \to \mathsf { K I } ( P ) _ { \mathrm { d e t } }$ 

Conversely, suppose that $\mathsf { D } \to \mathsf { K I } ( P ) _ { \mathrm { d e t } }$ is an isomorphism. Our goal is now to show the unique existence of the dashed arrow in diagram (3.10). We observe that the arrow $f \colon A \to P X$ represents an arrow $A  X$ in $\mathsf { K I } ( P )$ . The commutativity of the outer square entails that this arrow is deterministic, so that there is a unique preimage ${ \bar { f } } \colon A \to X$ in D. The condition that $\bar { f }$ is sent to $f$ is precisely the condition that the upper triangle commutes—the lower left triangle then commutes automatically by construction of the arrows. □ 

Example 3.5. Consider the distribution monad $D _ { R }$ valued in a commutative semiring R as in Example 3.3. Then depending on what R is, the diagram (3.8) for $P = D _ { R }$ may or may not be a pullback for all sets X. For example when $R = \mathbb { R } _ { + }$ we recover the usual distribution monad involving finitely supported probability measures, and (3.8) is a pullback since every {0, 1}-valued and finitely supported probability measure is a Dirac delta. 

The most trivial examples when (3.8) is not a pullback occur when δ does not have monomorphism components. For instance, if R is the zero semiring, then the associated distribution monad $D _ { R }$ on Set is the terminal monad, since every $D _ { R } X$ is a singleton set containing the unique map $X  R$ . In this case, it is clear that (3.8) is a pullback only when X itself is a singleton set. 

For a less trivial example, namely one in which $\delta \colon X \to P X$ is in fact injective but (3.8) is still not a pullback, let $P$ be the distribution monad $D _ { R \oplus R }$ for any nonzero commutative semiring R, where the addition and multiplication in $R \oplus R$ are component-wise. Consider the set $X : = \{ a , b \}$ and the distribution 

$$
s := (0, 1) \delta_ {a} + (1, 0) \delta_ {b} \in P X\tag{3.11}
$$

for $0 , 1 \ \in \ R .$ Clearly s is not a delta distribution, since the only two delta distributions in P X are $( 1 , 1 ) \delta _ { a }$ and $( 1 , 1 ) \delta _ { b }$ Nevertheless, both the product distribution $s \otimes s$ and $P ( { \mathrm { i d } } , { \mathrm { i d } } ) ( s )$ are equal to 

$$
(0, 1) \delta_ {(a, a)} + (1, 0) \delta_ {(b, b)} \in P (X \times X).\tag{3.12}
$$

Therefore, thinking of s as a morphism $I  P X$ in Set and using it in place of $f$ in diagram (3.10) proves that diagram (3.8) is not a pullback in this case. Although s is not a delta measure, s : $I  X$ is a deterministic morphism in $\mathsf { K I } ( D _ { R \oplus R } )$ , correctly capturing the intuition that s does not produce any randomness. 

A semiring R is entire if $R \not \cong 0$ and R has no zero divisors. We then have the following positive result. 

Proposition 3.6. For an entire commutative semiring R, the diagram (3.8) with $P = D _ { R }$ is a pullback for all X. 

Proof. Since δ has monomorphism components by $1 \neq 0$ in $R ,$ it is enough to prove that for every $r _ { 1 } , r _ { 2 } , s \in P X$ such that 

$$
r _ {1} \otimes r _ {2} = P (\mathrm{id}, \mathrm{id}) (s)\tag{3.13}
$$

holds, we necessarily have $r _ { 1 } = r _ { 2 } = s = \delta _ { x }$ for some $x \in X$ . Equation (3.13) unfolds to 

$$
r _ {1} (x _ {1})   r _ {2} (x _ {2}) = \left\{ \begin{array}{l l} s (x _ {1}) & \text { if } x _ {1} = x _ {2} \\ 0 & \text { otherwise } \end{array} \right.\tag{3.14}
$$

for all $x _ { 1 } , x _ { 2 } \ \in \ X$ . Since $\textstyle \sum _ { x _ { 1 } } r _ { 1 } ( x _ { 1 } )$ is equal to 1 by normalization, there must be an ${ \tilde { x } } \in X$ such that $r _ { 1 } ( \tilde { x } ) \neq 0$ . We then necessarily have $r _ { 2 } ( x _ { 2 } ) = 0$ for all $x _ { 2 } \neq \tilde { x }$ , because R is entire. Therefore, $r _ { 2 } ( \tilde { x } ) = 1$ by normalization; and applying the same argument the other way around yields the analogous statement for $r _ { 1 }$ , so that $r _ { 1 } = r _ { 2 } = \delta _ { \tilde { x } }$ , from which $s = \delta _ { \tilde { x } }$ follows as well. □ 

## 3.2 Markov Categories as Kleisli Categories

Many common Markov categories are indeed Kleisli categories of afine symmetric monoidal monads, as per Proposition 3.1. In this subsection, we prove a partial converse to this result. As we will see, the resulting representable Markov categories carry additional structure which we put to use in the rest of the paper: For every object $X$ , there is a distribution object P X, to be interpreted as the space of probability measures on the given space X. 

But let us start by asking under what conditions a given Markov category C arises from the construction of Proposition 3.1. If the monad P on D satisfies the assumption that (3.8) is a pullback, then Proposition 3.4 provides us with the natural bijection 

$$
\mathsf {K l} (P) _ {\det} (A, P X) \cong \mathsf {K l} (P) (A, X),\tag{3.15}
$$

intuitively stating that Markov kernels $A  X$ are in bijection with ordinary maps $A \to P X$ , where P X is the “object of distributions” on the object X. 

In particular, P uniquely extends to a right adjoint to the inclusion functor ${ \mathsf { K I } } ( P ) _ { \mathrm { d e t } } \hookrightarrow { \mathsf { K I } } ( P )$ , resulting in a functor $\mathsf { K I } ( P ) \to \mathsf { K I } ( P ) _ { \mathrm { d e t } }$ which we also denote $P$ by abuse of notation. On a Kleisli morphism represented by $f \colon X \to P Y$ in the original category $\mathsf { D } ,$ the naturality of equation (3.15) in X shows that this functor acts by assigning to it the corresponding morphism of free P -algebras, namely the composite 

$$
P X \xrightarrow {P f} P P Y \xrightarrow {E} P Y.
$$

In the probability context, the units and counits of the Kleisli adjunction (3.15) instantiate to maps intimately familiar from probability theory. The unit component $A  P A$ is of course the maps that assigns delta distributions. The counit $P X  X$ in $\mathsf { K I } ( P )$ , which is the Kleisli morphism represented by $\operatorname { i d } _ { P X } \colon P X \to P X$ , has been less commonly considered explicitly. It can be thought of as the Markov kernel $P X  X$ which assigns to every probability distribution $\mu \in P X$ a random element $\left( \mathrm { a \ ^ { * } s a m p l e ^ { \prime \prime } } \right)$ of X distributed according to $\mu .$ . We thus call it the sampling map and denote it by samp : $P X  X$ 

In summary, if $P$ is an afine symmetric monoidal monad satisfying the relevant pullback condition, then we obtain the natural bijection of (3.15). From right to left, a Markov kernel $A  X$ can be reinterpreted as a deterministic map $A  P X$ from left to right, composing a deterministic map $A \  \ P X$ by sampling from its output distribution produces a Markov kernel $A \  \ X$ . By construction, we have samp $\circ \delta = \mathrm { i d }$ , which can be interpreted to mean that sampling from a delta distribution $\delta _ { x }$ for $x \in X$ returns x. 

Based on these considerations, it is natural to consider bijections of the same type for arbitrary Markov categories now. 

Definition 3.7. Let C be a Markov category, and let $X ~ \in ~ \mathsf { C }$ be an object. A distribution object for X is an object P X equipped with a morphism $P X  X$ so that the induced map 

$$
\mathsf {C} _ {\mathrm{det}} (A, P X) \to \mathsf {C} (A, X)
$$

is a bijection for all $A \in \mathsf C$ 

In other words, P X is a distribution object if it represents the hom-functor 

$$
\mathsf {C} (\_, X): \mathsf {C} _ {\mathrm{det}} ^ {\mathrm{op}} \to \mathsf {S e t}
$$

in $\mathsf { C } _ { \mathrm { d e t } }$ . The distinguished morphism $P X \ \to \ X$ then arises as the morphism represented by $\operatorname { i d } _ { P X } \colon P X \to P X$ . As before, we call it the sampling map, denoted by 

$$
\mathsf {s a m p}: P X \to X,
$$

also writing samp whenever we want to emphasize the dependence on X. Furthermore, $\operatorname { i d } _ { X } \colon X \to X$ is classified by a deterministic morphism $\delta \colon X \to P X$ , which is characterized as being the unique deterministic morphism $X  P X$ satisfying samp $\circ \delta = \mathrm { i d }$ 

Notation 3.8. We write $( \_ ) ^ { \sharp } \colon { \mathsf { C } } ( A , X ) ~ \to ~ { \mathsf { C } } _ { \mathrm { d e t } } ( A , P X )$ for the inverse of the bijection samp $^ { \circ } - \cdot$ . Explicitly, for any $f \colon A \to X , f ^ { \sharp }$ is the composite 

$$
A \xrightarrow {\delta} P A \xrightarrow {P f} P X.\tag{3.16}
$$

Note that the term “distribution object” is motivated by the fact that the global elements $I  X$ in C, which are the abstract versions of probability distributions on $X ,$ , correspond to the global elements $I  P X$ in $\mathsf { C } _ { \mathrm { d e t } }$ 

Lemma 3.9. If every $X \in \mathsf C$ has a distribution object P X, then the assignment $X \mapsto P X$ is the object part of a functor $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ which is right adjoint to the inclusion $\mathsf C _ { \mathrm { d e t } } \hookrightarrow \mathsf C$ , and with the counit of the adjunction being the transformation whose components are the sampling maps. 

Proof. This is part of the standard theory of adjunctions. 

The faithfulness of the left adjoint $\mathsf C _ { \mathrm { d e t } } \hookrightarrow \mathsf C$ also implies that the unit components $\delta \colon X \to P X$ are all monomorphisms [26, Lemma 4.5.13]. 

Definition 3.10. A Markov category is termed representable $i f$ every object has a distribution object. We call the corresponding right adjoint functor $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ the distribution functor for C. 

Of course, if ${ \mathsf C } = { \mathsf K } | ( P )$ is a Markov category arising from the construction of Proposition 3.1 and the monad $P$ satisfies the pullback condition of Equation (3.8), then C is representable. 

If C is a representable Markov category, then the defining adjunction induces a monad on $\mathsf { C } _ { \mathrm { d e t } }$ . We denote its underlying functor also by $P \colon { \mathsf { C } } _ { \mathrm { d e t } } \to { \mathsf { C } } _ { \mathrm { d e t } } .$ , since it difers from $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ merely by restriction to the subcategory $\mathsf { C } _ { \mathrm { d e t } }$ . This monad has unit $\delta$ and multiplication P samp. Indeed, in the probability context, sampling from the “inner” distribution of a distribution of distributions returns the expected distribution, which is consistent with the idea that P samp is the multiplication of a probability monad. In fact, we can also compose $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ with the inclusion functor on the other side, considering $P$ as a functor $\mathsf C \to \mathsf C$ instead. Hence, $P$ comes in three versions which we do not distinguish notationally; we leave it understood that $P$ can act on any morphism of C and always returns a deterministic morphism. 

Remark 3.11. However, an important caveat is that $\delta$ is a natural transformation between id : $\mathsf { C } _ { \mathrm { d e t } } \to \mathsf { C } _ { \mathrm { d e t } }$ and $P \colon \mathsf { C } _ { \mathrm { d e t } } \to \mathsf { C } _ { \mathrm { d e t } }$ , and in particular natural with respect to deterministic morphisms. But δ is generally not natural with respect to nondeterministic morphisms. This is one way in which denoting the two functors $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ and $P \colon \mathsf { C } _ { \mathrm { d e t } } \to \mathsf { C } _ { \mathrm { d e t } }$ by the same letter may be initially confusing. 

On the other hand, the sampling transformation samp from $P \colon { \mathsf { C } } \ \to \ { \mathsf { C } }$ to id : $\mathsf C \to \mathsf C$ is natural with respect to all morphisms in C. In particular, the diagram 

$$
\begin{array}{c} P P X \xrightarrow {P _ {\text { samp }}} P X \\ \text { samp } \Biggl \downarrow \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \Biggl \downarrow_ {\text { samp }} \\ P X \xrightarrow {\text { samp }} X \end{array}\tag{3.17}
$$

commutes for all $X \in \mathsf C$ , which amounts to the usual associativity of the monad multiplication. 

For every representable Markov category C with distribution functor $P _ { \mathrm { : } }$ , there is a canonical isomorphism ${ \mathsf { C } } \cong { \mathsf { K I } } ( P )$ . This is an instance of the elementary fact that if any identity-on-objects functor $\mathsf { D } _ { 1 } \to \mathsf { D } _ { 2 }$ has a right adjoint, then this makes $\mathsf { D } _ { 2 }$ canonically isomorphic to the Kleisli category of the induced monad on $\mathsf { D } _ { 1 } . { } ^ { 7 }$ 

However, the Markov category structure on C equips this monad with additional structure and properties. Next, we show that P is an afine symmetric monoidal monad in a canonical way and that it automatically satisfies the pullback condition of Proposition 3.4. As a consequence, if the right adjoint of $\mathsf C _ { \mathrm { d e t } } \hookrightarrow \mathsf C$ exists, then the canonical isomorphism of categories ${ \mathsf { C } } \cong \mathsf { K I } ( P )$ is in fact an isomorphism of Markov categories. 

Proposition 3.12. Let C be a representable Markov category. Then the right adjoint $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ has a canonical symmetric lax monoidal structure which makes the adjunction between P and the inclusion functor $\iota \colon \mathsf C _ { \mathrm { d e t } } \ \hookrightarrow \ \mathsf C$ into a symmetric monoidal adjunction. 

The proof is best understood as an instance of the general theory of doctrinal adjunctions [20]. 

Proof. Since both composites and monoidal products of deterministic morphisms are again deterministic, and also all monoidal structure isomorphisms are deterministic, we can equip $\mathsf { C } _ { \mathrm { d e t } }$ with the monoidal structure induced from C, and this makes the inclusion functor $\iota \colon \mathsf { C } _ { \mathrm { d e t } } \hookrightarrow \mathsf { C }$ into a strict symmetric monoidal functor by definition. 

By the general theory of doctrinal adjunctions,<sup>8</sup> a right adjoint to a strong monoidal functor is canonically lax monoidal, and the structure maps are given as follows: 

• For all objects X and $Y$ of $\mathsf { C } ,$ the multiplication map $\nabla$ of the functor $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ is given by 

$$
\nabla : P X \otimes P Y \xrightarrow {\delta} P (P X \otimes P Y) \xrightarrow {P (\mathsf {s a m p} \otimes \mathsf {s a m p})} P (X \otimes Y),
$$

which is deterministic due to being a composite of deterministic morphisms. Naturality of $\nabla$ means that the following diagram ought to commute for all (not necessarily deterministic) morphisms $f \colon X \to Y$ and $g \colon A  B$ 

$$
\begin{array}{l} P X \otimes P A \xrightarrow {\delta} P (P X \otimes P A) \xrightarrow {P (\mathsf {s a m p} \otimes \mathsf {s a m p})} P (X \otimes A) \\ \Biggl \downarrow_ {P f \otimes P g} \qquad \qquad \Biggl \downarrow_ {P (P f \otimes P g)} \qquad \qquad \Biggl \downarrow_ {P (f \otimes g)} \\ P Y \otimes P B \xrightarrow {\delta} P (P Y \otimes P B) \xrightarrow {P (\mathsf {s a m p} \otimes \mathsf {s a m p})} P (Y \otimes B) \end{array}
$$

The left square commutes by naturality of $\delta$ with respect to the deterministic morphism $P f \otimes P g$ and the right one by naturality of samp, so that $\nabla$ is indeed natural in both arguments. This can be interpreted as the fact that processing two independent random variables independently preserves their independence. 

A straightforward but tedious diagrammatic argument, involving the given properties of $\delta$ and samp including samp ◦ $\delta = \mathrm { i d }$ , then shows that the relevant associativity condition for $\nabla$ to be a lax monoidal structure holds as well. Compatibility with the braiding $X \otimes Y \to Y \otimes X$ is obvious. 

• The natural isomorphism 

$$
\mathsf {C} _ {\mathrm{det}} (X, P I) \cong \mathsf {C} (X, I)
$$

shows that $P I \cong I$ by the assumed terminality of I. The unit $I  P I$ is thus the unique morphism of this type, and it automatically satisfies the relevant compatibility conditions with the multiplication. 

Hence, the right adjoint $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ is a symmetric lax monoidal functor. It remains to be shown that $\delta$ and samp, as unit and counit of the adjunction, are monoidal transformations. 

The fact that $\delta$ is a monoidal natural transformation means that the following diagram 

$$
\begin{array}{c} X \otimes Y \xrightarrow {\delta \otimes \delta} P X \otimes P Y \\ \Biggl \downarrow_ {\delta} \qquad \qquad \qquad \qquad \Biggl \downarrow_ {\nabla} \\ P (X \otimes Y) \end{array}
$$

commutes. This can be interpreted as the fact that products of Dirac deltas are again Dirac deltas. A formal proof follows via a standard naturality argument together with samp $\circ \delta = \mathrm { i d }$ 

Dually, the fact that samp is a monoidal natural transformation means that the diagram 

$$
\begin{array}{c} P X \otimes P Y \xrightarrow {\nabla} P (X \otimes Y) \\ \text {samp} \otimes \text {samp} \end{array} \begin{array}{c} \Big \downarrow \text {samp} \\ X \otimes Y \end{array}
$$

commutes. This can be interpreted as the fact that sampling from a product distribution is the same as sampling from the two marginals independently, and again follows formally by similar arguments. □ 

Remark 3.13. The strength of the monoidal monad P is given by the deterministic maps $\sigma _ { X , Y } : X \otimes P Y \to P ( X \otimes Y )$ , natural in $\mathsf { C } _ { \mathrm { d e t } } .$ , given by the composition 

$$
X \otimes P Y \xrightarrow {\delta \otimes \mathrm{id}} P X \otimes P Y \xrightarrow {\nabla} P (X \otimes Y).
$$

The strength satisfies the following commutative diagram, 

$$
\begin{array}{c} X \otimes P Y \xrightarrow {\sigma} P (X \otimes Y) \\ \text { id } \otimes \text { samp } \quad \downarrow \text { samp } \\ X \otimes Y \end{array}\tag{3.18}
$$

which has a similar, but “one-sided”, interpretation to the analogous condition for ∇. Note that, since the unit δ of the adjunction is not natural on the whole of C (Remark 3.11), the strength $\sigma \colon X \otimes P Y \to P ( X \otimes Y )$ is natural with respect to general morphisms only in the second argument, and natural with respect to deterministic morphisms in the first argument. 

Corollary 3.14. Let C be a representable Markov category. Then the monad (P, P samp, δ) on $\mathsf { C } _ { \mathrm { d e t } }$ arising from the underlying adjunction is symmetric monoidal and afine, thus inducing an isomorphism of Markov categories ${ \mathsf { C } } \cong \mathsf { K I } ( P )$ 

Proof. We have already noted that there is a canonical isomorphism of categories ${ \mathsf { C } } \cong { \mathsf { K I } } ( P )$ . It is also an isomorphism of monoidal categories because the defining adjunction $\mathsf { C } _ { \mathrm { d e t } } ( A , P X ) \cong \mathsf { C } ( A , X )$ is monoidal. Finally, to see that the copy maps are preserved, it is enough to note that on both sides, they are given by the diagonals $Y  Y \times Y$ in the cartesian monoidal category $\mathsf { C } _ { \mathrm { d e t } }$ □ 

Lemma 3.15. Let C be a representable Markov category with distribution functor P . Then P satisfies the pullback condition of Proposition 3.4 on $\mathsf { C } _ { \mathrm { d e t } }$ 

Proof. We need to show that for every $A , X \in \mathsf C$ and any diagram in $\mathsf { C } _ { \mathrm { d e t } }$ of the form 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/3028de42eff1a0ba0d1026a64c53b0aaf5bb1787c3f7b375ffcb6faf3f171684.jpg)


(3.19) 

without the dashed arrow, there is a unique dashed arrow such that the diagram commutes. Note that the diagonal in $\mathsf { C } _ { \mathrm { d e t } }$ is given by the copy map in $\mathsf { C } ,$ so that the two vertical morphisms in the diagram are 

$$
(\delta , \delta) = (\delta \otimes \delta) \circ \operatorname{copy} _ {X}, \quad P (\mathrm{id}, \mathrm{id}) = P (\operatorname{copy} _ {X}).\tag{3.20}
$$

Since $\delta$ is a monomorphism by samp $\circ \delta = \mathrm { i d }$ , the uniqueness is automatic and it is enough to find some $g$ which makes the diagram commute. 

To this end, note first that composing the whole diagram with the two marginalization maps $P ( X \otimes X ) \to P X$ shows that $f _ { 2 } = ( f _ { 1 } , f _ { 1 } )$ , again as a pairing with respect to the universal property of $P X \otimes P X$ as a product in $\mathsf { C } _ { \mathrm { d e t } }$ 

We now show that $g : = { \mathsf { s a m p } } \circ f _ { 1 }$ does the job. To this end, it is enough to prove that $g$ is deterministic, because then we have 

$$
\delta \circ g = P g \circ \delta\tag{3.21}
$$

resulting in commutativity of the upper triangle by 

$$
P g \circ \delta = P \mathsf {s a m p} \circ P f _ {1} \circ \delta = f _ {1} \circ \mathsf {s a m p} \circ \delta = f _ {1}\tag{3.22}
$$

Commutativity of the lower left triangle then also follows, thanks to $f _ { 2 } = ( f _ { 1 } , f _ { 1 } )$ 

The claim that $g$ is deterministic amounts to the commutativity of the outermost rectangle in the diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/9628197ea03971ed63da227a5d1c08009a086e05f5c414d6a06922ee6251bdfe.jpg)


Here, the lower left triangle commutes by $f _ { 2 } = ( f _ { 1 } , f _ { 1 } )$ , the oddly shaped square by assumption, the upper right square by naturality of samp and the lower right triangle by Proposition 3.12. Therefore, choosing $g$ to be samp $\circ f _ { 1 }$ makes the diagram (3.19) commute. □ 

We can summarize the previous results as follows. 

Theorem 3.16. For a Markov category C, the following are equivalent: 

1. C is representable. 

2. There is an afine symmetric monoidal monad P on $\mathsf { C } _ { \mathrm { d e t } }$ such that: 

• The diagram (3.8) is a pullback for every $X$ . 

• The identity functor on $\mathsf { C } _ { \mathrm { d e t } }$ extends to an isomorphism of Markov categories ${ \mathsf { C } } \cong { \mathsf { K I } } ( P )$ 

In particular, since representability is a property rather than extra structure, the monoidal monad P in the second condition is unique (up to unique isomorphism). 

This result is similar, but unrelated, to [5, Theorem 4.7], where a correspondence is drawn between Freyd categories and Kleisli categories of strong (not necessarily commutative) monads. 

Proof. If C is representable, Lemma 3.9 gives us the desired monad $P ,$ and the isomorphism of Markov categories is the one of Corollary 3.14. Finally, Lemma 3.15 states exactly that this monad satisfies the pullback condition. 

For the converse, we only need to show that the inclusion functor $\mathsf C _ { \mathrm { d e t } } \hookrightarrow \mathsf C$ has a right adjoint. This holds by the assumed isomorphism ${ \mathsf { C } } \cong { \mathsf { K I } } ( P )$ together with the Kleisli adjunction, which gives us natural bijections 

$$
\mathsf {C} _ {\mathrm{det}} (A, P X) \cong \mathsf {K l} (P) (A, X) \cong \mathsf {C} (A, X).
$$

Note that the pullback condition is not needed in this argument. 

Example 3.17. If C is a representable Markov category, then every parametric Markov category ${ \mathsf { C } } _ { W }$ as introduced in Section 2.2 is representable too. One can use the same distribution objects and take the sampling map ${ \mathsf { S a m p } } _ { X }$ in ${ \mathsf { C } } _ { W }$ to be represented by de $\mathsf { l } _ { W } \otimes \mathsf { s a m p } _ { X }$ , resulting in the desired bijection 

$$
\mathsf {C} _ {W, \det} (A, P _ {W} X) = \mathsf {C} _ {\det} (W \otimes A, P X) \cong \mathsf {C} (W \otimes A, X) = \mathsf {C} _ {W} (A, X).
$$

Thus, the distribution functor $P _ { W } \colon { \mathsf { C } } _ { W } \to { \mathsf { C } } _ { W , \mathrm { d e t } }$ acts the same on objects as the original $P \colon { \mathsf { C } }  { \mathsf { C } } _ { \mathrm { d e t } }$ does. The action on morphisms is then uniquely determined subject to making the bijection $\mathsf C _ { W , \mathrm { d e t } } ( A , P _ { W } X ) \cong \mathsf C _ { W } ( A , X )$ natural. Concretely, a morphism $f \in \mathsf C _ { W } ( A , X )$ represented by $f \colon W \otimes A \to X$ gets mapped to the morphism $P _ { W } f \in \mathsf C _ { W } ( P _ { W } A , P _ { W } X )$ represented by the composite 

$$
W \otimes P A \xrightarrow {\sigma} P (W \otimes A) \xrightarrow {P f} P X,\tag{3.23}
$$

where $\sigma \colon W \otimes P A \to P ( W \otimes A )$ denotes the strength of the monad P as introduced in Remark 3.13. 

In order to see that this is how $P _ { W }$ must act on morphism in ${ \mathsf { C } } _ { W }$ , it is enough to show that this prescription indeed makes the bijection 

$$
\mathsf {C} _ {W, \mathrm{det}} (A, P _ {W} X) \cong \mathsf {C} _ {W} (A, X)
$$

natural in X. That is, we need to check that for each morphism $k \colon X \to Y$ represented by $k \colon W \otimes X \to Y$ , the following diagram 

$$
\begin{array}{c c c} \mathsf {C} _ {W, \mathrm{det}} (A, P _ {W} X) & \xrightarrow [ \cong ]{\text {sampo-}} & \mathsf {C} _ {W} (A, X) \\ \Biggl \downarrow_ {P _ {W} k \circ_ {-}} & & \Biggl \downarrow_ {k \circ_ {-}} \\ \mathsf {C} _ {W, \mathrm{det}} (A, P _ {W} Y) & \xrightarrow [ \cong ]{\text {sampo-}} & \mathsf {C} _ {W} (A, Y) \end{array}
$$

commutes. Starting with a deterministic $f \colon W \otimes A \to P X$ in the top-left corner, commutativity of the diagram amounts to showing that the equation 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7d00d19c17ef52a77c27edf178c4fc704411450ff0b5a0bbaa281ab4935c08d1.jpg)


(3.24) 

holds in C, where we use (3.23) in order to express $P _ { W }$ k in terms of $P k$ and $\sigma .$ This equation follows straightforwardly if we apply the naturality of samp and property (3.18). 

## 3.3 Almost-Surely-Compatible Representability

In a representable Markov category, it is not a priori clear whether the defining equation $\mathsf C _ { \mathrm { d e t } } ( A , P X ) \cong \mathsf C ( A , X )$ respects almost sure equality, in the following sense. An almost sure equality of two deterministic morphisms $A \to P X$ (with respect to some morphism $p \colon \Theta \to A )$ implies the corresponding almost sure equality of the resulting morphisms $A  X$ , since the latter are obtained simply by composition with the sampling morphisms $P X  X$ . However, the other direction is not clear: 

If two morphisms $A  X$ are almost surely equal, does this means that also their deterministic counterparts $A \to P X$ must be almost surely equal? 

Indeed, in Example 3.23 we provide a representable Markov category in which this converse implication fails to hold. But since such a converse is relevant to our upcoming applications of representable Markov categories, we now investigate representable Markov categories in which it does hold. 

Definition 3.18. A Markov category is a.s.-compatibly representable if it is representable and for any morphism $p \colon \Theta \to A$ , the defining natural bijection 

$$
\mathsf {C} _ {\mathrm{det}} (A, P X) \cong \mathsf {C} (A, X)
$$

respects almost sure equality. That $i s ,$ for all $f , g \colon A \to X$ , we have 

$$
f ^ {\sharp} = _ {p - a. s.} g ^ {\sharp} \qquad \Longleftrightarrow \qquad f = _ {p - a. s.} g.\tag{3.25}
$$

As we already noted, the implication from left to right is automatic because of $f = \mathsf { s a m p } f ^ { \sharp }$ 

Many representable Markov categories are actually a.s.-compatibly representable, including BorelStoch as the following example shows. 

Example 3.19. For any two $f , g \colon A \to X$ in BorelStoch, we have $f = _ { p \mathrm { - } \mathrm { a . s . } } ~ g$ if and only if for all $S \subseteq \Sigma _ { A }$ and $T \subseteq \Sigma _ { X }$ 

$$
\int_ {S} f (T | a) p (d a | \theta) = \int_ {S} g (T | a) p (d a | \theta),\tag{3.26}
$$

or equivalently if and only if the two functions $f ( T | \_ ) , g ( T | \_ ) \colon A \to \mathbb { R }$ are $p ( \mathrm { \_ } { \cdot } | \theta ) { \cdot } \mathrm { a . s }$ equal for every $\theta \in \Theta$ and every $T \in \Sigma _ { X }$ [12, Example 13.3]. What we need to prove is that this holds uniformly in T , i.e., that the measures $f ( \_ { a } )$ and $g ( \_ { a } )$ are likewise $p ( \underline { { \mathbf { \delta \mu } } } _ { - } | \theta )$ -almost surely equal with respect to $a \in A$ . Since $\Sigma _ { X }$ is countably generated, say by a sequence of measurable sets $( T _ { n } ) _ { n \in \mathbb { N } }$ , it is enough to show that $f ( T _ { n } | a ) = g ( T _ { n } | a )$ holds for all n with unit probability in a. But this is indeed the case by assumption, since a countable intersection of sets of full measure again has full measure. Therefore, BorelStoch is a.s.-compatibly representable. 

A property equivalent to a.s.-compatible representability, which is useful in manipulations of string diagrams, turns out to be the following. 

Definition 3.20. A representable Markov category is said to satisfy the sampling cancellation property if, for any three morphisms $f , g \colon X \otimes A \to Y$ and $h \colon A \to X$ the following implication holds: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/ed264d6003d35a1d657834ac47838ed871ff456fc2b60250ca1c8817b3d6baf1.jpg)


The name of this condition is explained by the equation $f = \mathsf { s a m p } f ^ { \sharp } ;$ , so that the implication amounts to the possibility to cancel the sampling map in diagram equations of the above form. 

Proposition 3.21. A representable Markov category C satisfies the sampling cancellation property if and only if it is a.s.-compatibly representable. 

Proof. If in Definition 3.20 we use $f , g \colon X \otimes A \to Y$ of the form $f \otimes \mathrm { d e l } _ { A }$ and $g \otimes \mathrm { d e l } _ { A }$ for arbitrary $f , g \colon X \to Y$ and $h = p ,$ then we recover the non-trivial direction of (3.25). 

Conversely, if in Definition 3.18 we use $p \colon A \to X \otimes A$ given by 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/94c689194ee28e329a19dd464ccf376c86c28f74da04e38c540dd300a2d37a8d.jpg)


(3.27) 

for a given $h \colon A \to X$ , then the right-to-left implication of (3.25) implies the sampling cancellation property. □ 

In Example 3.17, we saw that if a Markov category C is representable, then so is every parametric Markov category ${ \mathsf { C } } _ { W }$ . As the following lemma shows, the same can be said about a.s.-compatible representability. 

Lemma 3.22. Let C be an a.s.-compatibly representable Markov category. For every $W \in \mathsf C$ , the parametric Markov category ${ \mathsf { C } } _ { W }$ as introduced in Section 2.2 is likewise a.s.-compatibly representable. 

Proof. First of all, notice that if $f \in \mathsf C _ { W } ( A , X )$ is a morphism in ${ \mathsf { C } } _ { W }$ represented by $f \colon W \otimes A \to X$ in C, then its adjunct $f ^ { \sharp } \in { \mathsf { C } } _ { W } ( A , P _ { W } X )$ is represented by $f ^ { \sharp } \colon W \otimes A \to P X$ , the adjunct of f in C. This follows because $P _ { W } X$ is a distribution object of ${ \mathsf { C } } _ { W }$ with respect to the same sampling map as P X is in C. 

Therefore, the non-trivial part of checking a.s.-compatible representability of ${ \mathsf { C } } _ { W }$ i.e., the right-to-left implication of (3.25), boils down to the following implication 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/848cb3a5b983552b58149073e9d6f65da50ed597b3781b6254eec8c690e233ef.jpg)


(3.28) 


in C. This holds because C satisfies the sampling cancellation property by Proposition 3.21. Consequently, ${ \mathsf { C } } _ { W }$ is a.s.-compatibly representable. □


Example 3.23. We now give an example of a Markov category which is representable but not a.s.-compatibly representable. Continuing on from Proposition 3.6, the Kleisli category $\mathsf { K I } ( D _ { R } )$ of the distribution monad $D _ { R }$ for an entire commutative semiring R is representable with ${ \mathsf { K I } } ( D _ { R } ) _ { \mathrm { d e t } } = { \mathsf { S e t } }$ . As we elaborate below, there is an R such that $\mathsf { K I } ( D _ { R } )$ is not a.s.-compatibly representable. 

Concretely, let R be the semiring 

$$
R := \{0, \varepsilon , 1 \}\tag{3.29}
$$

with addition and multiplication given by the following nontrivial cases: 

$$
\begin{array}{c} {1 + 1 = 1, \quad 1 + \varepsilon = 1, \quad \varepsilon + \varepsilon = \varepsilon ,} \\ {\varepsilon^ {2} = \varepsilon .} \end{array}\tag{3.30}
$$

Intuitively, we can think of assigning value $1 \in R$ to outcomes that are possible and happen with nonzero probability; assigning ε to outcomes that may be considered, but whose probability is 0 or negligibly small; and assigning $0 \in R$ to outcomes that could never happen. Then the above arithmetical rules acquire straightforward interpretations. 

Since this commutative semiring R has idempotent addition and multiplication, it can also be understood as a distributive lattice with max as addition and min as multiplication. In this picture, R is simply the three-element totally ordered set with $0 < \varepsilon < 1$ . It is also clear that R is entire. 

In the representable Markov category $\mathsf { K I } ( D _ { R } )$ , we then consider $A = X = \{ a , b \}$ together with $f , g \colon A  A$ represented by the morphisms $f ^ { \sharp } , g ^ { \sharp } \colon A  P A$ given by 

$$
\begin{array}{l l} f ^ {\sharp} (a) := \delta_ {a}, & f ^ {\sharp} (b) := \varepsilon \delta_ {a} + \delta_ {b}, \\ g ^ {\sharp} (a) := \delta_ {a}, & g ^ {\sharp} (b) := \delta_ {a} + \varepsilon \delta_ {b}. \end{array}
$$

We also consider $p \colon I  A$ represented by $p ^ { \sharp } : = \delta _ { a } + \varepsilon \delta _ { b }$ . Then we have $f ^ { \sharp } \neq _ { p - \mathrm { a . s . } } g ^ { \sharp }$ since 

$$
\delta_ {(a, \delta_ {a})} + \varepsilon \delta_ {(b, \varepsilon \delta_ {a} + \delta_ {b})} \neq \delta_ {(a, \delta_ {a})} + \varepsilon \delta_ {(b, \delta_ {a} + \varepsilon \delta_ {b})}.\tag{3.31}
$$

However, applying sampling to the second output reduces this to 

$$
\delta_ {(a, a)} + \varepsilon^ {2} \delta_ {(b, a)} + \varepsilon \delta_ {(b, b)} = \delta_ {(a, a)} + \varepsilon \delta_ {(b, a)} + \varepsilon^ {2} \delta_ {(b, b)},\tag{3.32}
$$

where the equation holds by $\varepsilon ^ { 2 } = \varepsilon$ . Therefore, we have $f = _ { p \mathrm { - } \mathrm { a . s . } } ~ g$ and $\mathsf { K I } ( D _ { R } )$ is not a.s.-compatibly representable. 

## 4 Second-Order Stochastic Dominance

In this and the following sections, we state and prove generalizations of existing concepts in probability theory and statistics to representable Markov categories. The first one for which we do this is second-order stochastic dominance. Traditionally, this is a partial order of probability distributions on <sup>R</sup> or <sup>Rn</sup> that expresses whether a given distribution is more “spread out” than another. 

In the abstract setting of representable Markov categories, second-order dominance makes sense for all algebras A of the monad P on $\mathsf { C } _ { \mathrm { d e t } }$ . It is concerned with comparing two distributions on A, represented now by morphisms $p , q \colon I  A$ , and induces a preorder relation on $\mathsf { C } ( I , A )$ . More generally, it is a preorder relation on every hom-set $\complement ( \Theta , A )$ , defined in terms of the P -algebra structure on A. 

One way to define second-order dominance in terms of the existence of a so-called dilation $A  A$ that takes q to p. Intuitively, a dilation is a specific kind of map which increases uncertainty without afecting the expected value of distributions on A. 

Definition 4.1. Let C be a representable Markov category and let e: $P A  A$ be an algebra of the monad $( P , \delta , P \mathsf { s a m p } )$ on $\mathsf { C } _ { \mathrm { d e t } }$ . Then, given a morphism $f \colon \Theta \to A$ in C, a morphism $t \colon \Theta \otimes A \to A$ is an f -dilation (with respect to the P -algebra 

structure e) if it satisfies 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/d9700da88e77ede7b72d650ff2906c94bc8336fc1c7d526497dab44efeb05f9d.jpg)


(4.1) 


Thus, in case $\Theta$ is the unit object, an f -dilation t has to satisfy


$$
e \circ t ^ {\sharp} = _ {f \mathrm{-a.s.}} \mathrm{id}.\tag{4.2}
$$

In the probability theory context, such dilations are also called mean-preserving maps, as the following example elucidates. 

Example 4.2. Given the choice of C = BorelStoch and a compact set ${ \mathit { A } } \subseteq \mathbb { R }$ , the canonical algebra map e: $P A  A$ is the assignment of expectation values. Relative to it, an f -dilation is any Markov kernel t : $A  P A$ that takes f -almost every point $a \in A$ to a distribution $t ^ { \sharp } ( a )$ whose expectation value is $a$ itself. Similarly, for a compact $A \subseteq \mathbb { R } ^ { n }$ , or for a closed and bounded subset of a separable Banach space, the natural choice of $e \colon P A \to A$ is one that maps each distribution to its barycenter. 

For general Θ, equation (4.1) in BorelStoch becomes 

$$
e \big (t (\_ | \theta , a) \big) = a\tag{4.3}
$$

for $f ( \_ { \theta } )$ -almost all $a \in A$ and all $\theta \in \Theta$ . This again matches the intuition that the distribution $t ( \_ { \theta , a ) }$ dilates the point a, suitably almost surely, but now for every $\theta \in \Theta$ separately. 

Remark 4.3. Throughout this section, we could restrict to the case $\Theta = I$ only, and then instantiate our definitions and results on the parametric Markov category $C _ { \Theta }$ in order to recover the additional parameter dependence on any $\Theta \in \mathsf { C } .$ . We have decided against doing so for the benefit of making the greater generality of our formalism more explicitly apparent. 

When working with second-order dominance, it is often helpful to assume a.s.- compatible representability rather than mere representability, which we do from now on. 

Lemma 4.4. Let C be an a.s.-compatibly representable Markov category. Consider the free algebra P X of the monad $( P , P \mathsf { s a m p } , \delta )$ on $\mathsf { C } _ { \mathrm { d e t } }$ , with algebra map 

$$
P s a m p: P P X \rightarrow P X,
$$

and a morphism $f \colon \Theta \to P X$ in C. Then $t \colon \Theta \otimes P X \to P X$ is an f -dilation if and only if it satisfies 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7fb606dba9956112ee6a385996ce68d56aa2c995de8029ecc63d2fef7749dc4b.jpg)


(4.4) 

Proof. Equation (4.4) follows from (4.1) for $e ~ = ~ P { \mathsf { s a m p } } .$ , namely by applying $\operatorname { i d } _ { P X } \otimes \mathsf { s a m p } _ { X }$ to it and using the commutativity of diagram (3.17) together with samp $\circ t ^ { \sharp } = t$ 

Conversely, since the sampling cancellation property follows from a.s.-compatible representability by Proposition 3.21, we can follow the same reasoning backwards<sup>10</sup> and conclude the equation 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/aeaaa22d180cce04a4ab5fcf8a764c1e7ac2d0bcaf548f76f80359a8478a15e8.jpg)


(4.5) 

as was to be shown. 

As the following proposition shows, the existence of dilations that convert between morphisms can be related to the existence of partial evaluations [13]. 

Proposition 4.5. Let C be an a.s.-compatibly representable Markov category with distribution functor P and for which conditionals exist. Then for any P -algebra $e \colon P A \ \to \ A$ in $\mathsf { C } _ { \mathrm { d e t } }$ and any morphisms $p , q \colon \Theta \ \to \ A$ in C, the following two conditions are equivalent: 

(i) There exists a morphism $r \colon \Theta \ \to \ P A$ such that the following diagram commutes: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/a7b6f0dc972df33ceb8498ccd58c14d3a978d092d044dec70cffc1cd5866c142.jpg)


(4.6) 

(ii) There exists a q-dilation $t \colon \Theta \otimes A \to A$ which converts q to p in the following sense: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/fa783f51535e0129f076f262764d533be0bdb98285bfd5210ddabe5f357d8c77.jpg)


(4.7) 

Proof. We split the proof into two parts each consisting of one of the implications. 

$( \mathrm { i } ) \Rightarrow ( \mathrm { i i } )$ : Given an $r \colon \Theta \to P A$ that makes the diagram (4.6) commute, we construct s : $A \otimes \Theta \to A$ as a conditional of the morphism 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/078d9c49421fa1ac0ee099222ccc3bd24bdbb2eaa34c3c21a6621866aefb41f9.jpg)


(4.8) 

with respect to the left output, so that the defining equation of conditionals 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/9267a359db7d0e0c712c8ddd26492e4b5753b1c42f2d8e1a54144bd73d93693a.jpg)


(4.9) 

holds. Upon defining $t ~ : = ~ \mathsf { s a m p } _ { A } \circ \ s ,$ the property (4.7) then follows immediately by applying del $_ A \otimes \operatorname { i d } _ { P A }$ to equation (4.9). 

It remains to be shown that t is a q-dilation. Applying $\operatorname { i d } _ { A } \otimes e$ to equation (4.9), we get 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/cb454cccb496823e86a75ecd333ced1585b8b39c699211b26033bd2d53f198db.jpg)


(4.10) 

where the second step uses the assumption that e is deterministic. Applying the sampling cancellation property, we obtain 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/ac076104f1cc47df3024e3cbda8291823299bb23e665c8864b52d5a0e91004b9.jpg)


(4.11) 

Now the fact that $t ^ { \sharp } = { \cal P } { \mathsf { s a m p } } \circ s ^ { \sharp }$ satisfies equation (4.1) follows by applying $\operatorname { i d } _ { A } \otimes e$ to equation (4.11) and using the fact that e is a P -algebra: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/ef0f00c12b4cd9f3f24571024872f569cc200e4c90e834e6487dd0c5cf8f1945.jpg)


(4.12) 


Thus, we have shown the implication $( \mathrm { i } ) \Rightarrow ( \mathrm { i i } )$


$( \mathrm { i i } ) \Rightarrow ( \mathrm { i } )$ : Given a morphism $t \colon \Theta \otimes A \to A$ satisfying (4.7) and (4.1), we define r via 

$$
\begin{array}{c c} P A & \\ \boxed {r} & := \\ \Theta & \end{array} \quad \begin{array}{c c} t ^ {\sharp} & \\ \boxed {q} & \end{array}\tag{4.13}
$$

Applying samp to this equation yields 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/e791e9b0c562d30c7826657184ba00e9ef0eadfbf27db6553fdfbc14317a5cf5.jpg)


(4.14) 

whence ${ \mathsf { s a m p } } _ { A } r = p$ follows by virtue of the fact that t converts q to $p _ { \cdot }$ . 

On the other hand, applying e to equation (4.13) gives $e \circ r \ : = \ : q$ by the assumption that t is a q-dilation with respect to e. □ 

Definition 4.6. If the equivalent conditions of Proposition 4.5 hold, then we say that $q$ second-order dominates p with respect to $e ,$ and denote this relation as 

$$
p \sqsubseteq q.\tag{4.15}
$$

By Example 4.2, this recovers the usual notion of second-order stochastic dominance for probability measures on any compact $A \subseteq \mathbb { R } ^ { n }$ if we take C to be BorelStoch and $\Theta = I$ 

## 5 Comparison of Statistical Experiments

## 5.1 Informativeness of Statistical Experiments

Dilations also appear in the context of comparison of statistical experiments, as introduced by Blackwell [2]. In this case, statistical experiments are modeled by families of measures indexed by a parameter set Θ that labels the distinct hypotheses one aims to discern by performing the experiment. Here, we represent statistical experiments abstractly as morphisms $\Theta \to X$ in a Markov category. 

Commonly, the question of comparing two experiments $f , g$ in terms of whether f is more informative about Θ than g is, amounts to the existence of a map c satisfying $c f = g$ . We can interpret c as a post-processing of the data generated by experiment $f$ in a way that produces the data of experiment g. If such $\mathrm { ~ a ~ c ~ }$ exists, we refer to it as garbling map and say that f is more informative than $^ { g , }$ denoted by $f \succeq g .$ . A slightly more general version of this notion was introduced by Golubtsov in [17]. 

The informativeness ordering defined via garbling maps can be equivalently expressed in terms of loss functions or Bayesian utilities in decision theory. For an account of the origins of this equivalence, see [22, Section 3] for example. Recently, it has also been expressed in categorical terms by de Oliveira in [11]. 

In what follows, we make use of the following relaxed informativeness ordering relative to a particular prior m : $I  \Theta$ 

Definition 5.1. Given morphisms m: $I \ \to \ \Theta , \ f \colon \Theta \ \to \ X$ and $g \colon \Theta \ \to \ Y$ in any Markov category $\mathsf { C } ,$ we say that f is $m { \mathrm { - a . s . } }$ . more informative than $g ,$ , denoted $f \succeq _ { m - a . s . } g ,$ if there exists a morphism c : $X  Y$ such that we have $c f = _ { m - a . s . ~ g }$ 2 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/544e333e934e16868264b00df598cdc313de24e22e13e174cf1718095644ffa3.jpg)


(5.1) 

Note that the informativeness orderings are actually preorders on the collection of morphisms out of $\Theta .$ , but we use the term “ordering” as synonymous with “preordering”. 

Example 5.2. For a concrete example, consider a company that manufactures metal rods. After production, a selection of rods is tested for structural integrity. The hypothesis space $\Theta = \{ \mathsf { s } , \mathsf { f } \}$ thus consists of two possibilities: Either the selected rod is safe (s) or it is faulty (f). 

There are two tests available. The threshold test g checks whether the rod withstands hanging a weight from its midpoint, while the oscillation test $f$ checks whether the rod withstands transverse oscillations of a certain type. Each test has two possible outcomes: Either the rod passes $( \checkmark )$ or fails $( \times )$ the test, so that we have $X = Y = \{ { \sqrt { , \times } } \}$ . According to our model of metal rods and their defects (that we assume to be correct, up to the experimental precision) the outcomes of the two tests are generally distributed as follows: 

$$
g (\checkmark | \mathsf {s}) = 0. 7 2, \qquad g (\checkmark | \mathsf {f}) = 0. 4 5,
$$

$$
f (\checkmark | \mathsf {s}) = 0. 9 6, \qquad f (\checkmark | \mathsf {f}) = 0. 6,
$$

$$
g (\times | \mathsf {s}) = 0. 2 8, \qquad g (\times | \mathsf {f}) = 0. 5 5,
$$

$$
f (\times | \mathsf {s}) = 0. 0 4, \qquad f (\times | \mathsf {f}) = 0. 4.
$$

However, suppose that the test results cannot be trusted when both are executed on the same rod, for example because either test may aflict structural damage to the rod even upon passing the test. Then only one of $g$ or $f$ can be performed, and we are interested to know whether doing one of the experiments provides us with strictly more information about whether a given rod is safe. To that end, we can use the ordering $\succeq .$ . In particular, we have $f \succeq g$ , because the stochastic map 

$$
\begin{array}{l} c (\checkmark | \checkmark) = 0. 7 5 \\ c (\times | \checkmark) = 0. 2 5 \end{array}
$$

$$
\begin{array}{l} {c (\checkmark | \times) = 0} \\ {c (\times | \times) = 1} \end{array}
$$

achieves the conversion of the oscillation test to the threshold test by garbling. 

Remark 5.3. The informativeness ordering and its approximate versions that we leave out of our analysis here are particularly interesting in situations when the two experiments $f$ and $g$ cannot be implemented jointly or when it is costly to do so. They tell one which of the two mutually exclusive choices for an experiment is a better choice as far as learning about the hypothesis Θ is concerned. 

On the other hand, if one could execute both f and $g$ simultaneously, a more relevant question may be that of whether $f \ \left( \mathrm { o r } \ g \right)$ is more informative than their joint implementation, which would be an experiment $h \colon \Theta \to X \otimes Y$ with marginals $f$ and $g .$ In practice, X and Y need not be conditionally independent given Θ. However, it is customary to assume so, in accordance with the assumption that Θ constitutes a complete set of relevant parameters. The joint experiment can then be expressed as 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/1348185dfc0ae9c383c2949d28ab598ac2b0596e7236a4b13a4e22bb3f6ecfc4.jpg)


(5.2) 

It is not hard to see that with this kind of joint implementation, the relation between $f$ and g induced by $f \succeq _ { m - \mathrm { a . s . } }$ h is diferent from the basic informativeness ordering $f \succeq _ { m - \mathrm { a . s . } } g$ . Nevertheless, as Theorem 5.4 below shows, the latter is closely connected to the question of whether X (or Y ) constitutes a suficient statistic for $X \times Y$ , but the joint implementation of $f$ and g is not in general the one given by equation (5.2) (in particular, see the left equation of (5.4)). 

The considerations in the paragraph above do not necessarily take into account that there might be a cost associated with performing the experiments, which would make the comparison of the information contained in two samples (one from X and one from Y ) with that of one sample (from X, say) less meaningful. Instead, if one compares the same number of samples, either one from X or one from Y , then the relevant relation is the basic informativeness ordering given by $f \succeq _ { m - \mathrm { a . s . } } g .$ 

A slightly diferent context in which the informativeness ordering is relevant is the theory of communication. There, we commonly interpret f and g as distinct encodings of Θ in X and Y respectively. In general, f and g lose some of the information contained in Θ. The preorder  then tells us which of the two encodings unambiguously retains more of this information, and whether such a comparison can be made at all. 

A measure-theoretic version the following theorem appears in [27, Theorem 7.2.16], but its roots can be traced back to [1]. 

Theorem 5.4. Let m: $I \to \Theta , f \colon \Theta \to X$ and $g \colon \Theta \to Y$ be morphisms in a Markov category C. If C has conditionals, then the following are equivalent: 

(i) f is m-a.s. more informative than g. 

(ii) There exists a morphism h : $\Theta \to X \otimes Y$ with marginals m-almost surely given by f and g respectively, such that the deterministic morphism $\operatorname { i d } _ { X } \otimes \operatorname { d e l } _ { Y }$ is a suficient statistic for h. 

(iii) There exists a morphism µ : $I \to \Theta \otimes X \otimes Y$ satisfying 

(a) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/d09f3f452bf9330cefdee3dab9f5fa6531a76014fc5c0b1e088e6cd236918f79.jpg)


(b) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/b560a70538dddcd48a91fd1d866940dc0af0699e2340f38a247194b70747ad2b.jpg)


(c) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/a381676a3eda1c733e3e8650121f30d13a6ef3b199eb4b22f9a69fd705f963e1.jpg)


(d) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7c0ab6e409d4cdc11f0da88f4dd1d612fea88d9563cecc9fac932a589505216e.jpg)


The reading of condition (b) is that there are some morphisms that can take place of the empty boxes so that the equation holds. In other words, it states that µ displays the conditional independence [12, Definition 12.1] of Θ and Y given X. 

Also note that conditions (c) and (d) are independent of the choice of conditionals by the a.s.-uniqueness of conditionals. 

Proof. We split the proof into three implications. 

(i) ⇒ (ii): The condition that $\operatorname { i d } _ { X } \otimes \operatorname { d e l } _ { Y }$ is a suficient statistic for $h \ [ 1 2$ , Definition 14.3] translates to the existence of a morphism α : $X  X \otimes Y$ such that 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/51bf32d3ca5f8f239b7f354d3a6ffeb354fe4f426e8f3c51437d5bff5e44ad6f.jpg)


(5.3) 

holds. Assuming condition (i) is true, we can use the garbling map c satisfying equation (5.1) to define the requisite h and α via 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/39b980322be9f6a2a284b21e091b900dd5461a8caff0606e8bb8f2f34bb0247d.jpg)


(5.4) 

from which equation (5.3) follows. Since the marginals of h so defined are f and g respectively (the latter m-almost surely), we obtain the desired implication $( \mathrm { i } ) \implies \mathrm { ( i i ) }$ 

(ii) ⇒ (iii): We can define a morphism $\mu$ in terms of h and m as follows: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/9db1132db5f8f07f1d3b425dd7e6b92bce886069b128e580d176d70636f50237.jpg)


(5.5) 

Conditions $( a ) , ( c )$ , and (d) are then immediate. In order to show that condition (b) holds as well, we can use equation (5.3) with the middle output marginalized 

to get 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/288c405d946161f9acf081833de22d8fa36be6c7d1a02715c699b391e6960d74.jpg)


(5.6) 

where the second equation follows from assuming condition (ii), in particular from the fact that the $\Theta \to X$ marginal of $h$ is $m { \mathrm { - a . s . } }$ . equal to $f .$ In order to obtain condition (b), we can then apply the definition of a Bayesian inverse of $f$ with respect to m to get 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/45432f7d451892c8a96c4d9c3023e27d463d850317a90f609f49183a50d18e1b.jpg)


(5.7) 

as required. Consequently, condition (ii) indeed implies condition (iii). 

$( \mathrm { i i i } ) \Rightarrow ( \mathrm { i } )$ : Let the decomposition of $\mu$ as given by condition (b) be 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/309a50757751046b804558a8ec08398cf73e5ad9fcb10b6c7d8f0059948be0dd.jpg)


(5.8) 

It remains to show that the morphism $c \colon X \to Y$ from such a decomposition can act as the garbling that achieves the conversion of $f$ to $g _ { ; }$ m-almost surely. Taking the conditional of equation (5.8) and using k $n = m$ , which follows from 

condition (a), yields 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/8f7c1570c268ad64fe8fb11141d612af6352fc6f113c71159f38da709bb0dbcc.jpg)


(5.9) 

where $k ^ { \dagger }$ denotes the Bayesian inverse of k with respect to n. Marginalizing over $Y$ in equation (5.9) and using condition $( c )$ then gives $k ^ { \dagger } = _ { m - \mathrm { a } . \mathrm { s } . } f$ . Finally, by marginalizing equation (5.9) over X and using condition $( d )$ , we arrive at $g = _ { m - \mathrm { a . s . } } c f$ and the proof is thus complete. □ 

## 5.2 The Classical Blackwell–Sherman–Stein Theorem

Insofar as there is a host of equivalent ways to characterize the informativeness ordering [22, Theorem 1], we are interested in the extent to which one can generalize these results to the abstract setting of Markov categories and proved with synthetic methods. We already saw an instance of such a result in the form of Theorem 5.4, which relates informativeness to suficient statistics and conditional independence. For the remainder of Section 5, we focus on the Blackwell–Sherman– Stein Theorem [2, Theorem 6], also known as the dilation criterion. It states that the informativeness order $\succeq$ for statistical experiments coincides with the secondorder stochastic dominance order of the so-called standard measures on $P \Theta$ , the description of which we turn to now. 

An intuitive way to think of standard measures is to interpret a statistical experiment $f \colon \Theta \ \to \ X$ as a way of learning about the underlying hypothesis represented by the parameter set Θ. From this perspective, given a prior $m \in P \Theta$ one can use Bayesian updating to find the corresponding posterior on $P \Theta$ , which of course depends on the value of X observed. Thus, it can be represented by the measurable map $( f ^ { \dagger } ) ^ { \sharp } \colon X \to P \Theta$ . The standard measure is then an element of $P P \Theta$ obtained as a mixture of these posteriors with respect to the chosen prior $m ,$ or more precisely, with respect to the distribution of $X$ one would expect, were the “true” value of the hypothesis Θ sampled from $m$ 

The morphism given by the composite 

$$
\Theta \xrightarrow {f} X \xrightarrow {(f ^ {\dagger}) ^ {\sharp}} P \Theta\tag{5.10}
$$

is commonly referred to as the standard experiment $\hat { f }$ of $f .$ Intuitively, for a given “true” hypothesis as input, the standard experiment outputs the distribution over posteriors that results from conducting the experiment and applying Bayesian updating. Since the outcome of the experiment itself is random, we obtain a distribution over posteriors rather than a mere posterior. Therefore, the standard experiment is typically not deterministic and it clearly depends on the prior m. One can then also think of the standard measure as $\hat { f }$ applied to m. 

Example 5.5. Traditionally, one uses a uniform prior m to define standard measures for finite parameter sets, but any strictly positive probability measure would do. Continuing our Example 5.2 and choosing a uniform prior 

$$
m (\mathsf {s}) = 0. 5
$$

$$
m (\mathsf {f}) = 0. 5
$$

gives the following posteriors (expressed as functions rather than Markov kernels): 

$$
\begin{array}{r l} & {\left(g ^ {\dagger}\right) ^ {\sharp} (\checkmark) = \frac {0 . 7 2 \delta_ {\mathrm{s}} + 0 . 4 5 \delta_ {\mathrm{f}}}{0 . 7 2 + 0 . 4 5} \approx 0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}}} \\ & {\left(g ^ {\dagger}\right) ^ {\sharp} (\times) = \frac {0 . 2 8 \delta_ {\mathrm{s}} + 0 . 5 5 \delta_ {\mathrm{f}}}{0 . 2 8 + 0 . 5 5} \approx 0. 3 4 \delta_ {\mathrm{s}} + 0. 6 6 \delta_ {\mathrm{f}}} \\ & {\left(f ^ {\dagger}\right) ^ {\sharp} (\checkmark) = \frac {0 . 9 6 \delta_ {\mathrm{s}} + 0 . 6 \delta_ {\mathrm{f}}}{0 . 9 6 + 0 . 6} \approx 0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}}} \\ & {\left(f ^ {\dagger}\right) ^ {\sharp} (\times) = \frac {0 . 0 4 \delta_ {\mathrm{s}} + 0 . 4 \delta_ {\mathrm{f}}}{0 . 0 4 + 0 . 4} \approx 0. 0 9 \delta_ {\mathrm{s}} + 0. 9 1 \delta_ {\mathrm{f}}.} \end{array}
$$

The expected distributions of test outcomes if exactly half of the rods were faulty are 

$$
\begin{array}{l} g \circ m (\checkmark) = 0. 5 g (\checkmark | \mathsf {s}) + 0. 5 g (\checkmark | \mathsf {f}) = 0. 5 8 5 \\ g \circ m (\times) = 0. 5 g (\times | \mathsf {s}) + 0. 5 g (\times | \mathsf {f}) = 0. 4 1 5 \\ f \circ m (\checkmark) = 0. 5 f (\checkmark | \mathsf {s}) + 0. 5 f (\checkmark | \mathsf {f}) = 0. 7 8 \\ f \circ m (\times) = 0. 5 f (\times | \mathsf {s}) + 0. 5 f (\times | \mathsf {f}) = 0. 2 2 \end{array}
$$

Therefore the standard measures of $g$ and $f ,$ denoted by $\hat { g } _ { m }$ and $\hat { f } _ { m }$ respectively, are given by 

$$
\begin{array}{r} \hat {g} _ {m} \approx 0. 5 8 5 \delta_ {0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}}} + 0. 4 1 5 \delta_ {0. 3 4 \delta_ {\mathrm{s}} + 0. 6 6 \delta_ {\mathrm{f}}}, \\ \hat {f} _ {m} \approx 0. 7 8 \delta_ {0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}}} + 0. 2 2 \delta_ {0. 0 9 \delta_ {\mathrm{s}} + 0. 9 1 \delta_ {\mathrm{f}}}. \end{array}
$$

Explicitly, one can express the classical version of the BSS Theorem as follows. 

Theorem 5.6 (Blackwell–Sherman–Stein [22]). Let Θ, X, and Y be standard Borel spaces with Θ finite. For any two Markov kernels $f \colon \Theta \to X$ and $g \colon \Theta \to Y$ , the following are equivalent: 

1. $f \succeq g$ , i.e., f is more informative about Θ than g is. 

2. $\hat { f } _ { m } \subseteq \hat { g } _ { m } , i . e .$ , the standard measure of g second-order dominates the standard measure of $f$ 

Example 5.7. In terms of our running example of metal rods, we saw that $f$ is more informative than $g$ in Example 5.2 and constructed the standard measures in Example 5.5. Theorem 5.6 says that there should be a $\hat { g } _ { m } { \mathrm { - d i l a t i o n } }$ $t \colon P \Theta \to P \Theta$ that maps $\hat { g } _ { m }$ to $\hat { f } _ { m } .$ , meaning that the posteriors according to the oscillation test $f$ are “more spread out” than those corresponding to the threshold test $g .$ Concretely, a dilation that does the job can be chosen to be any measurable map $t ^ { \sharp }$ satisfying 

$$
0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}} \mapsto \delta_ {0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}}}
$$

$$
0. 3 4 \delta_ {\mathrm{s}} + 0. 6 6 \delta_ {\mathrm{f}} \mapsto 0. 4 7 \delta_ {0. 6 2 \delta_ {\mathrm{s}} + 0. 3 8 \delta_ {\mathrm{f}}} + 0. 5 3 \delta_ {0. 0 9 \delta_ {\mathrm{s}} + 0. 9 1 \delta_ {\mathrm{f}}}
$$

up to our convention of rounding to two decimal places. One can use Lemma 4.4 to convince oneself that these relations indeed give a ${ \hat { g } } _ { m } \mathrm { - d i l a t i o n \ } t ,$ since we have 

$$
0. 3 4 \approx 0. 4 7 * 0. 6 2 + 0. 5 3 * 0. 0 9, \quad 0. 6 6 \approx 0. 4 7 * 0. 3 8 + 0. 5 3 * 0. 9 1.
$$

One of the strong points of this result is that it allows one to reduce the comparison of experiments $\Theta \to X$ for arbitrary $X$ to the comparison of measures on a fixed sample space, namely P Θ. 

## 5.3 The Blackwell–Sherman–Stein Theorem in Markov Categories

Our goal is now to state and prove a version of Theorem 5.6 for Markov categories. In order to arrive at such a synthetic generalization, we need a bit more than just a representable Markov category. Indeed, the requirements are the same as in Proposition 4.5. 

Assumption 5.8. Throughout the rest of Section 5, let C be an a.s.-compatibly representable Markov category with conditionals, as well as $f \colon \Theta \to X$ and $g \colon \Theta \to Y$ arbitrary morphisms in C with the same domain. 

We mention this assumption again in the statements of our results, but otherwise leave it implicit. 

The existence of conditionals is necessary in order to have an abstract notion of Bayesian inference, which is used to construct the basic elements of the BSS Theorem: standard experiments and standard measures. The representability is relevant again for the definition of the standard experiment and standard measure, which make reference to the distribution functor P . The a.s.-compatibility, in the sense of Definition 3.18, is relevant for proving a.s. uniqueness of the standard experiment, and for the interpretation of the second condition of the upcoming Theorem 5.13 as a second-order dominance relation via Lemma 4.4. 

Next, we present the definitions of standard experiment and standard measure in the language of Markov categories. 

Definition 5.9. Given morphisms m: $I  \Theta$ and $f \colon \Theta \to X$ in a Markov category C with conditionals, the standard experiment ${ \hat { f } } \colon \Theta \to P \Theta$ of f is given by 

$$
\begin{array}{c c} P \Theta & \\ \framebox {\hat {f}} & := \\ \Theta & \end{array} \qquad \begin{array}{c c} P \Theta & \\ \framebox {(f ^ {\dagger}) ^ {\sharp}} & \\ \framebox {f} & \\ \Theta & \end{array}\tag{5.11}
$$

where $f ^ { \dagger } \colon X \to \Theta$ is a Bayesian inverse of f with respect to m. 

Standard experiments are unique, m-almost surely, as long as the Markov category is a.s.-compatibly representable and has conditionals. To see this, consider two Bayesian inverses of $f$ with respect to m, $f _ { 1 } ^ { \dagger }$ and $f _ { 2 } ^ { \dagger }$ , which thus have to satisfy 

$$
\begin{array}{c c} \boxed {f _ {1} ^ {\dagger}} & = \\ \boxed {f} & \boxed {f} \\ \hline m & \end{array}\tag{5.12}
$$

by the definition of Bayesian inverses. Applying the sampling cancellation property and the causality property [12, Definition 11.30] which follows from the existence of 

conditionals [12, Proposition 11.33] gives 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/4e7b99203c31a67def174f2f111abe16eb88896785ec2ff53a3e7ec9162155b0.jpg)


(5.13) 

which is exactly the equation needed to conclude that $\hat { f }$ is well-defined up to ma.s. equality. 

Definition 5.10. The standard measure ${ \hat { f } } _ { m } \colon I \to P \Theta$ of f is then defined by 

$$
\begin{array}{c c c} P \Theta & \\ \bigtriangledown_ {\hat {f} _ {m}} & := & P \Theta \\ & & \boxed {\hat {f}} \\ & & m \end{array} = \begin{array}{c c c} \hline (f ^ {\dagger}) ^ {\sharp} \\ \hline f \\ \hline m \end{array}\tag{5.14}
$$

Per the m-almost sure uniqueness of ${ \hat { f } } ,$ the standard measure $\hat { f } _ { m }$ is unique as soon as C is a.s.-compatibly representable. 

Having introduced the basic necessary ingredients of the theory of comparison of statistical experiments and the BSS Theorem in the language of Markov categories, we now present the results that build up to the BSS Theorem itself, assuming throughout that we are in an a.s.-compatibly representable Markov category with conditionals. 

Lemma 5.11. Let $f \colon \Theta \to X$ be a morphism with standard experiment ${ \hat { f } } \colon \Theta \to P \Theta$ as defined above. Then the sampling map sam $\mathsf { p } _ { \Theta } \colon P \Theta \to \Theta$ is a Bayesian inverse of $\hat { f }$ with respect to m, i.e. we have 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/9318be5d7f9672d48949aa67cbe6498d3d32a81f58e426063206f03325836369.jpg)


(5.15) 

Proof. Since, by definition, $( f ^ { \dagger } ) ^ { \sharp }$ is deterministic and satisfies samp $\circ ( f ^ { \dagger } ) ^ { \sharp } = f ^ { \dagger }$ , we can prove the lemma as follows: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/d35a9d76f1252346f0d775aeed801cbe5623a5051a3f6f27ed8b4f6fa0450e23.jpg)


(5.16) 

The terminology “standard experiment” of $\hat { f }$ is then justified by the following result, which states that $\hat { f }$ is exactly as informative about $\Theta$ as the original experiment $f$ is, at least up to m-a.s. equality. 

Proposition 5.12. For any $f _ { i }$ , we have $f \succeq { \hat { f } }$ and $\hat { f } \succeq _ { m - a . s . } f$ 

In standard measure-theoretic probability, this is [27, Proposition 7.2.2]. 

Proof. Since $f \succeq \hat { f }$ is clear from the definition of the standard experiment, the crux of the proof lies in showing that there exists a morphism $r \colon P \Theta \to X$ such that $r \hat { f } = _ { m - \mathrm { a . s . } } f$ . That is, $r$ is a garbling map which recovers $f$ from its standard version. We now show that choosing $r$ to be a Bayesian inverse of $( f ^ { \dagger } ) ^ { \sharp }$ with respect to $f$ m does the job. With this choice, we thus have 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/efc3c0b62ee55fd9fa08d78af1a3ebf3410e225762724b9c61b89356fa5cc0b8.jpg)


(5.17) 

by the definition of Bayesian inverses. 

Applying sam ${ \mathsf { \Pi } } | { \mathsf { p } } _ { \Theta } \otimes { \mathrm { i d } } _ { X }$ to this equation yields 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/4d6306bf6114f6e9a8e1fbc8ece5d27bb8c6db73bf7f21ae5db717c2c35abf34.jpg)


(5.18) 

for its left-hand side and 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/80286f81da1ccb58fa2e546e0b772562ad342136f3a57ea6668d1699f2d1ced9.jpg)


(5.19) 

for its right hand side, where we use Lemma 5.11 to obtain the latter. Consequently, $f$ is m-almost surely equal to $r \hat { f } ,$ as we wanted to show. □ 

Now we have all the necessary ingredients to present a proof of our version of the Blackwell—Sherman—Stein Theorem in representable Markov categories. 

Theorem 5.13 (Blackwell—Sherman—Stein). Let C be an a.s.-compatibly representable Markov category with conditionals. Consider two morphisms $f \colon \Theta \to X$ and $g \colon \Theta \to Y$ in C, whose standard experiments are denoted by $\hat { f }$ and $\hat { g }$ respectively. 

Then the following are equivalent: 

1. $f \succeq _ { m - a . s . } g ,$ , i.e., there exists a morphism $c \colon X \to Y$ such that 

$$
c f = _ {m - a. s.} g.\tag{5.20}
$$

2. $\hat { f } _ { m } \subseteq \hat { g } _ { m }$ , i.e., there exists a ${ \hat { g } } _ { m } - d i l a t i c$ n t : $P \Theta \to P \Theta$ such that 

$$
\hat {f} _ {m} = t \hat {g} _ {m}.\tag{5.21}
$$

Proof. For the forward implication, let c : $P \Theta \to P \Theta$ be a morphism satisfying $c \hat { f } = _ { m - { \bf a } . { \bf s } . \mathrm { ~ } } \hat { g }$ , the existence of which is equivalent to $f \succeq _ { m - \mathrm { a . s . } } g$ by Proposition 5.12. 

We then prove that $\hat { f } _ { m } \subseteq \hat { g } _ { m }$ holds as well by constructing a $\hat { g } _ { m }$ -dilation that witnesses this second-order dominance relation. Let $c ^ { \dagger }$ denote the Bayesian inverse of $c$ with respect to $\hat { f } _ { m }$ . Then $c ^ { \dagger }$ satisfies equation (5.21) by definition. In order to show that $c ^ { \dagger }$ is a $\hat { g } _ { m } { \mathrm { - d i l a t i o n } }$ , we can use Lemma 5.11 twice: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/8bab81418879dde10b4887f92a7218dde026084200a642ef921c6b6e55e32dff.jpg)


(5.22) 

Overall, $c ^ { \dagger }$ is thus a $\hat { g } _ { m }$ -dilation that maps $\hat { g } _ { m }$ to ${ \hat { f } } _ { m } ,$ , as was to be shown. 

For the converse implication, suppose that a ${ \hat { g } } _ { m } .$ -dilation t with $\hat { f } _ { m } = t \hat { g } _ { m }$ exists, and denote its Bayesian inverse with respect to $\hat { g } _ { m }$ by $t ^ { \dagger }$ . We can now use the same steps as in the computation above in order to show that $t ^ { \dagger }$ achieves the conversion of $\hat { f }$ into $\hat { g } _ { ; }$ , at least m-almost surely: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7195a5b3d99fe4e6ca23b51cb3dc614b403d9cebaca7d6616da247a033523c0f.jpg)


(5.23) 

We have thus shown that $t ^ { \dagger }$ achieves the conversion $\hat { f } \succeq _ { m - { \mathrm { a . s . } } } \hat { g }$ and consequently we get $f \succeq _ { m - \mathrm { a . s . } } g$ by Proposition 5.12. □ 

Traditionally, the BSS Theorem is stated with exact equalities rather then almost surely with respect some measure $m \in \mathsf C _ { \mathrm { d e t } } ( I , P \Theta )$ . This is because the theorem is usually applied to finite (or countably infinite) parameter sets Θ, for which there exists a distribution $m \colon I  \Theta$ having full support, so that m-almost sure equality coincides with plain equality, 

$$
f = _ {m \mathrm{-a.s.}} g \quad \Longleftrightarrow \quad f = g\tag{5.24}
$$

for all $f , g \colon \Theta  A$ to any other object A. Thanks to this property, one can then remove all m-a.s. qualifications. This generalizes as follows. 

Definition 5.14. An object Θ of a Markov category is termed discrete if there exists a morphism m: $I  \Theta$ such that (5.24) holds for all $f , g \colon \Theta \to A$ to any A. 

Clearly such an m dominates every other $\mu \colon I  \Theta$ in the sense of Definition 2.8. In BorelStoch, the only standard Borel spaces Θ for which such an m exists are the discrete measurable spaces, meaning that Θ must be finite or countably infinite. Then one can choose m to be any distribution of full support on Θ, where in the case of finite Θ the uniform distribution is the commonly used choice. 

For discrete objects, we get the following version of the BSS Theorem, which is closer to the traditional account than Theorem 5.13. 

Corollary 5.15. Let C be an a.s.-compatibly representable Markov category with conditionals, and let Θ be a discrete object of C with respect to m: $I \to \Theta$ . Consider two morphisms $f \colon \Theta \to X$ and $g \colon \Theta \to Y$ in C, whose standard experiments are denoted by <sup>ˆ</sup>f and $\hat { g }$ respectively. 

Then the following are equivalent: 

1. $f \succeq g$ , i.e., there exists a morphism $c \colon X \to Y$ such that 

$$
c f = g.\tag{5.25}
$$

2. $\hat { f } _ { m } \subseteq \hat { g } _ { m } , i . e .$ , there exists a ${ \hat { g } } _ { m } - d i l a t i$ on t : $P \Theta \to P \Theta$ such that 

$$
\hat {f} _ {m} = t \hat {g} _ {m}.\tag{5.26}
$$

As far as we know, there is no established genuine generalization of the BSS Theorem beyond discrete parameter sets Θ. In Theorem 5.13, we have given a version of the theorem that goes beyond discrete parameters by virtue of using a.s. equality with respect to a measure m. In the specific case of BorelStoch, the possibility of doing this has been known, see for example [22]. However, we believe that our synthetic treatment exposes the key reasons for this to be the case and can therefore catalyze further development. 

Arguably, the more interesting aspect of our Theorem 5.13 is the fact that it applies in a much wider context than the traditional measure-theoretic one. In particular, we have shown that the result can be used in any Markov category that 

• allows one to perform Bayesian inference—i.e., one that has conditionals, and 

• can describe spaces of measures internally—i.e., one that is a.s.-compatibly representable. 

So far, we have not even begun to explore the full scope of this type of result. We explore one particular application in the next subsection. 

## 5.4 The Blackwell–Sherman–Stein Theorem Parametrized by Priors

In this subsection, we show that there is a (synthetic) version of the BSS Theorem which 

• holds for an arbitrary hypothesis object Θ, and 

• does not reference to any particular prior $m .$ , 

in contrast to Theorem 5.13 and Corollary 5.15, which only satisfy one of these requirements each. The catch is that, in general, it characterizes a slightly diferent informativeness ordering, and can be thought of as a version of Theorem 5.13 which is uniform in the prior. Interestingly, this result actually arises as a special case of Theorem 5.13, namely when the latter is instantiated in a parametric Markov category as introduced in Section 2.2. 

As before, we think of $f$ and g as statistical experiments with hypothesis space or parameter space Θ. Given the corresponding distribution object P Θ associated to the hypothesis space Θ, we then consider the parametric Markov category $\mathsf { C } _ { P \Theta }$ Intuitively, we think of morphisms in $\mathsf { C } _ { P \Theta }$ as Markov kernels parametrized by a prior over the hypothesis space Θ. Throughout this section, we use a.s. equality in $\mathsf { C } _ { P \Theta }$ with respect to the global element prsamp $\in \mathsf C _ { P \Theta } ( I , \Theta )$ represented by the sampling map: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/5a6a5ab0e3ea45b635e2f87c307c92a7eceb2c081b015a9c2e6a021046f63719.jpg)


(5.27) 

We think of this morphism as sampling a hypothesis in $\Theta$ distributed in accordance with the prior (which is not fixed here, but rather an extra parameter). 

Before we discuss the BSS Theorem instantiated in $\mathsf { C } _ { P \Theta }$ , we consider how the basic notions of comparison of statistical experiments look in $\mathsf { C } _ { P \Theta }$ when we reexpress them in terms of the corresponding morphisms in C. 

First of all, the statistical models $\Theta  X$ are thought of as models of the behavior of a system as a function of a model parameter $\Theta ,$ typically not under the experimenter’s control. The point of the theory of statistical experiments is to formalize and quantify the procedure of making inferences about an unknown parameter $\Theta$ by virtue of learning the value of X. We thus still assume that the statistical models in $\mathsf { C } _ { P \Theta }$ are morphisms independent of the prior P Θ and are therefore represented by 

$$
\begin{array}{c c c} A & & A \\ \square & = & \square \\ \Theta & & P \Theta \end{array}\tag{5.28}
$$

For better readability in future expressions in the C-representation, we introduce a new notation for the prior behavior f : $P \Theta \to \Theta \otimes X$ of a statistical model $f$ as follows 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/264e7e4fbb035b00cacb62ae9abc6340686740b313d2aa5148265b8c7886c932.jpg)


(5.29) 

The morphism f describes what a Bayesian experimenter expects to observe: For each prior distribution over hypotheses, it returns as outputs an experiment outcome, for a hypothesis randomly sampled from the prior, together with that hypothesis. 

The process of Bayesian updating itself is then described by 

$$
\left(\mathfrak {f} _ {| X}\right) ^ {\sharp}: X \otimes P \Theta \longrightarrow P \Theta ,
$$

where ${ \mathfrak { f } } _ { | X }$ denotes a conditional of f with respect to X. The deterministic morphism $( \mathfrak { f } _ { | X } ) ^ { \sharp }$ takes an outcome and a prior as input and returns the associated Bayesian posterior. Since conditionals are not unique in general, this Bayesian updating map is not uniquely determined by $f$ itself. As before, Bayesian updating features in the upcoming definition of the standard experiment. 

But let us consider the comparison of statistical experiments in $\mathsf { C } _ { P \Theta }$ first. Interpreting Definition 5.1 in $\mathsf { C } _ { P \Theta }$ , the prsamp-a.s. informativeness ordering of two prior-independent morphisms as in equation (5.28) says that $f \succeq _ { \mathsf { p r s a m p - a . s . } } g$ if and only if there exists $c \colon X \otimes P \Theta  Y$ such that we have 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/54e153d5ef0f7aaf07956f63d62c2f7537de45c6b205b46ee955f05cad678d99.jpg)


(5.30) 

This amounts to allowing the garbling map c in the definition of the informativeness ordering to depend on the prior in addition to its dependence on the data variable of the experiment $f$ used to simulate g. Since the condition (5.30) gives rise to an ordering on morphisms of C that difers from those considered in Sections 5.1 and 5.3, we give it a new name. 

Notation 5.16. Given two morphisms f and g in a Markov category C with a common domain Θ, we say that f is more informative than g in the Bayesian sense, denoted $f \succeq _ { \mathrm { B a y e s } } g$ , if we have $f \succeq _ { \mathsf { p r s a m p - } a . s . }$ g in $\mathsf { C } _ { P \Theta }$ as expressed by the existence of a prior-dependent garbling c that achieves the conversion shown in equation (5.30). 

Before the exposition of our parametric BSS Theorem itself, we present some results on how the Bayesian informativeness ordering relates to the usual priorindependent one. While it is obvious that the existence of a prior-independent c with $c f = g$ implies the existence of a prior-dependent c as above—namely by choosing that dependence to be the trivial one which discards the prior—the question of whether the converse also holds is far more involved. We start addressing it with the following simple observation, which shows that the garbling map can be chosen in a uniform way for all distributions which are dominated by a given one. 

Proposition 5.17. Let $\nu \colon I  \Theta$ be arbitrary. If f is more informative than g in the Bayesian sense, then there exists a morphism $c _ { \nu } \colon X \to Y$ in C such that we have $c _ { \nu } f = _ { \mu - a . s . } g , i . e .$ ， 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/11309af53c660fce1e4b2305e06f84e01b9b9f6239a85811699a365d1af83b70.jpg)


(5.31) 

for every $\mu \colon I  \Theta$ with $\mu \ll \nu$ 

Recall that $\mu \ll \nu$ denotes the dominance ordering of Definition 2.8. 

Proof. In particular, $c _ { \nu }$ can be constructed from c in equation (5.30) as 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/41958c7bd57bc18d5b4e1f520026dc78320458b35494d203dfb2db2650e35a38.jpg)


(5.32) 

which makes (5.31) hold with $\nu$ in place of $\mu .$ The claim then follows from the definition of $\mu \ll \nu$ □ 

Corollary 5.18. If the hypothesis object Θ is discrete, then 

$$
f \succeq g \quad \Longleftrightarrow \quad f \succeq_ {\text { Bayes }} g.
$$

Proof. Discreteness implies that there is a distribution $\nu \colon I  \Theta$ such that taking $\mu : = \nu$ makes $f \succeq g$ follow from equation (5.31). □ 

However, the existence of a prior-dependent garbling map does not imply the existence of a completely prior-independent one in general. We now present an explicit counterexample in BorelStoch based on an example due to Blackwell and Ramamoorthi [4]. 

Proposition 5.19. In BorelStoch, there are $f \colon \Theta \to X$ and $g \colon \Theta \to Y$ such that a garbling c satisfying equation (5.30) exists, but there is no Markov kernel c : $X  Y$ with $g = c f$ 

Proof. The following arguments amount to showing that the example of Blackwell and Ramamoorthi [4], which proved that classical suficiency and Bayesian suficiency are not equivalent, also similarly in our context of comparison of experiments. The main diference is that our version of their example requires a more refined measurability analysis in the second part. 

As the spaces of outcomes of the experiments, consider the two standard Borel spaces 

$$
X = \{a, b \} ^ {\mathbb {N}},
$$

$$
Y = \{a, b \}.
$$

Writing $\pi _ { n } \colon \{ a , b \} ^ { \mathbb { N } } \to \{ a , b \}$ for the n-th product projection, we define the sets 

$$
\Theta_ {a} := \Bigl \{\nu \in P X \Bigm | \lim _ {n \to \infty} \nu \bigl (\pi_ {n} ^ {- 1} (a) \bigr) = 1 \Bigr \},
$$

$$
\Theta_ {b} := \Bigl \{\nu \in P X \Big | \lim _ {n \to \infty} \nu \big (\pi_ {n} ^ {- 1} (b) \big) = 1 \Bigr \},
$$

to be thought of as containing those distributions for which the countably many $\{ a , b \}$ -valued random variables represented by a distribution on $X$ converge in probability to a or $b ,$ respectively. Since we have 

$$
\Theta_ {a} = \bigcap_ {k \in \mathbb {N}} \bigcup_ {n \in \mathbb {N}} \Bigl \{\nu \in P X \Bigm | \nu \bigl (\pi_ {n} ^ {- 1} (b) \bigr) \leq 2 ^ {- k} \Bigr \},
$$

the set $\Theta _ { a }$ is a measurable subset of P X, and we take it to be equipped with the induced σ-algebra. Moreover, it constitutes a standard Borel space since P X does too. A similar argument shows that $\Theta _ { b }$ is likewise a standard Borel space. 

We now consider the (disjoint) union $\Theta : = \Theta _ { a } \cup \Theta _ { b }$ , and let a measurable map $f \colon \Theta \to X$ be defined by the restriction of samp : $P X \to X { \mathrm { ~ t o ~ } } \Theta \subseteq P X$ , while the measurable map $g \colon \Theta \to Y$ is given by 

$$
g (\nu) := \left\{ \begin{array}{l l} a & \text { if } \nu \in \Theta_ {a}, \\ b & \text { if } \nu \in \Theta_ {b}. \end{array} \right.
$$

That is, $g ( \nu ) ~ = ~ a$ indicates that the sequence of random variables distributed according to $\nu$ converges in probability to $^ { a , }$ and similarly for $g ( \nu ) = b$ 

We first argue that there is no garbling from $f$ to ${ \mathit { g } } ,$ meaning that there is no Markov kernel $c \colon X \to Y$ with $g = c f$ . If such a c did exist, then one could define a measurable map $s \colon X  \{ a , b \}$ by 

$$
s (x) := \left\{ \begin{array}{l l} a & \text { if } c (\{a \} | x) > 0, \\ b & \text { if } c (\{a \} | x) = 0. \end{array} \right.
$$

Since for $\nu \in \Theta _ { a }$ we have $c ( \{ a \} \vert _ { - } ) = _ { \nu \mathrm { - } \mathrm { a . s . } } ~ 1$ , it follows that also $s = _ { \nu - \mathrm { a . s } }$ . a holds. Similarly, for every $\nu \in \Theta _ { b }$ we have $s = _ { \nu - { \mathrm { a . s . } } } \ b$ . However, Blackwell has shown in [3] that such an s does not exist, and therefore neither does c. 

Second, we construct a prior-dependent $c \colon X \otimes P \Theta \ \to \ Y$ such that equation (5.30) holds. In particular, note that even though Θ is defined so that the sequence of random variables converges in probability to either a or $b ,$ we cannot extract the limit from a sample sequence alone per the argument of the previous paragraph. We thus show that, given a prior $\mu \in P \Theta$ , one can always find a subsequence of the random variables that converges ν-almost surely for µ-almost all measures $\nu \in \Theta$ 

This requires a bit of preparation. For fixed $\mu \in \ P \Theta$ , consider the average measures defined for all $S \in \Sigma _ { X }$ as 

$$
\overline {{\nu}} _ {a} (S) := \int_ {\Theta_ {a}} \nu (S)   \mu (d \nu), \quad \overline {{\nu}} _ {b} (S) := \int_ {\Theta_ {b}} \nu (S)   \mu (d \nu).\tag{5.33}
$$

Note that these are both subnormalized, and that $\overline { { \nu } } _ { a } + \overline { { \nu } } _ { b }$ is exactly the expected probability measure $( P f ) ( \mu )$ on X. By the monotone convergence theorem, the assumed convergence in probability of the product projections still holds on average, i.e., we have 

$$
\lim _ {n \to \infty} \overline {{\nu}} _ {a} \big (\pi_ {n} ^ {- 1} (b) \big) = 0, \quad \lim _ {n \to \infty} \overline {{\nu}} _ {b} \big (\pi_ {n} ^ {- 1} (a) \big) = 0.\tag{5.34}
$$

For $k ~ \in ~ \mathbb { N }$ , let then $n _ { k } ( \mu )$ be the smallest natural number such that both the inequalities 

$$
\overline {{\nu}} _ {a} \big (\pi_ {n _ {k} (\mu)} ^ {- 1} (b) \big) \leq 2 ^ {- k} \quad \overline {{\nu}} _ {b} \big (\pi_ {n _ {k} (\mu)} ^ {- 1} (a) \big) \leq 2 ^ {- k}\tag{5.35}
$$

are satisfied. The existence of $n _ { k } ( \mu )$ is guaranteed by (5.34). 

We now show that the map $\mu \mapsto n _ { k } ( \mu )$ is measurable. To see this, notice that for every $m \in \mathbb { N }$ we have $n _ { k } ( \mu ) \leq m$ if and only if both 

$$
\int 1 _ {\Theta_ {a}} \nu (\pi_ {m} ^ {- 1} (b)) \mu (d \nu) \leq 2 ^ {- k} \quad \mathrm{and} \quad \int 1 _ {\Theta_ {b}} \nu (\pi_ {m} ^ {- 1} (a)) \mu (d \nu) \leq 2 ^ {- k}
$$

are satisfied. Preimages of the the upper sets $\{ m \mid k \leq m \} \subseteq \mathbb { N }$ are thus measurable by the inequalities above, because integration of a fixed measurable function on Θ is measurable in $\mu \in P \Theta$ . Since the discrete σ-algebra on <sup>N</sup> is generated by the upper sets, the assignment $\mu \mapsto n _ { k } ( \mu )$ is measurable. 

Thanks to inequalities (5.35) and the Borel-Cantelli lemma, we have that the measurable sets 

$$
\begin{array}{l} S _ {a} (\mu) := \left\{x \in X \mid \pi_ {n _ {k} (\mu)} (x) = a \text {for infinitely many} k \right\}, \\ S _ {b} (\mu) := \left\{x \in X \mid \pi_ {n _ {k} (\mu)} (x) = b \text {for infinitely many} k \right\}, \end{array}
$$

satisfy 

$$
\overline {{{{\nu}}}} _ {a} \big (S _ {b} (\mu) \big) = \overline {{{{\nu}}}} _ {b} \big (S _ {a} (\mu) \big) = 0.
$$

But since this must then also hold µ-almost surely for all the measures which form the averages $\overline { { \nu } } _ { a }$ and $\overline { { \nu } } _ { b }$ , it follows that $\nu ( S _ { b } ) = 0$ also holds for µ-almost all $\nu \in \Theta _ { a }$ a and similarly $\nu ( S _ { a } ) = 0$ for µ-almost all $\nu \in \Theta _ { b }$ . But then we can decide whether $\nu \in \Theta _ { a }$ or $\nu \in \Theta _ { b }$ simply by testing membership of its sample in $S _ { a }$ . In other words, the function 

$$
c \colon X \otimes P \Theta \to \{a, b \}, \qquad (x, \mu) \mapsto \left\{ \begin{array}{l l} a & \text { if } x \in S _ {a} (\mu), \\ b & \text { if } x \in \overline {{S _ {a} (\mu)}}, \end{array} \right.
$$

makes the desired equation (5.39) hold, since $c ( x , \mu ) = a$ for ν-almost every $x \in X$ and µ-almost every $\nu \in \Theta _ { a }$ , and similarly $c ( x , \mu ) = b$ for ν-almost every x and µ-almost every $\nu \in \Theta _ { b }$ 

It remains to be shown that c is actually measurable. This follows because the complement $\overline { { S _ { a } ( \mu ) } }$ is given by the countable disjoint union 

$$
\overline {{{{S _ {a} (\mu)}}}} = \bigcup_ {F} \left\{x \in \{a, b \} ^ {\mathbb {N}} \mid \pi_ {n _ {k} (\mu)} (x) = b \iff k \in F \right\}
$$

over finite $F \subseteq \mathbb { N }$ . Since for every fixed F the set of all pairs $( x , \mu )$ for which the internal condition holds is measurable by the measurability of $\mu \mapsto n _ { k } ( \mu )$ , the set of all pairs $( x , \mu )$ with $c ( x , \mu ) = b$ is likewise measurable. Therefore, c is measurable, thereby making f indeed more informative than g in the Bayesian sense. □ 

We continue with the general theory, aiming at a BSS Theorem for characterizing informativeness in the Bayesian sense. 

The standard experiment of a statistical model $f \colon \Theta \to X$ in $\mathsf { C } _ { P \Theta }$ , as introduced in Definition 5.9, now takes the form 

$$
\begin{array}{c c} P _ {P \Theta} \Theta & = \\ \boxed {\hat {f}} & = \\ \Theta & \end{array} \begin{array}{c c} P \Theta & \\ \hline (\mathfrak {f} | x) ^ {\sharp} & \\ \boxed {f} & \\ \Theta & P \Theta \end{array}\tag{5.36}
$$

Similar to before, this (typically non-deterministic) morphism takes a hypothesis as its first argument, a prior as its second argument, and outputs the distribution over posteriors which results if the given hypothesis is true and Bayesian updating is used with respect to the given prior. Again as before, in order for $\hat { f }$ to be well defined up to prsamp-a.s. equality, we need $\mathsf { C } _ { P \Theta }$ to be a.s.-compatibly representable as opposed to merely being representable. However, this is guaranteed by Assumption 5.8 and Lemma 3.22. 

Next, the standard measure $\hat { f } _ { \mathsf { p r s a m p } } : = \hat { f }$ ◦ prsamp in $\mathsf { C } _ { P \Theta }$ is represented in C by 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7330b0316254b04418dc11f64a029b73daf3cd16793cdd149debfe6d4da46766.jpg)


(5.37) 

and Lemma 5.11 becomes: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/82872a9c6837d4074e784bde772d7791dfd93322da5401180471f66c87174e53.jpg)


(5.38) 

Consequently, the statement of Theorem 5.13 in $\mathsf { C } _ { P \Theta }$ with respect to prsamp reads as follows. 

Corollary 5.20. Let C be an a.s.-compatibly representable Markov category with conditionals. Consider two morphisms $f \colon \Theta \to X$ and $g \colon \Theta \to Y$ in C with $\hat { f } _ { \mathsf { p r s a m p } }$ and $\hat { g } _ { \mathsf { p r s a m p } }$ given by the right hand side of equation (5.37). 

Then the following are equivalent: 

1. $f \succeq _ { \mathrm { B a y e s } } g .$ , i.e., there exists a morphism c : $X \otimes P \Theta \to Y$ satisfying 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/fcae3d2edba5ae9be549adc84d3f8fe0e233add480430e7fe6ec825156c76972.jpg)


(5.39) 

2. $\hat { f } _ { \mathsf { p r s a m p } } \subseteq \hat { g } _ { \mathsf { p r s a m p } }$ , i.e., there exists a $\hat { g } _ { \mathsf { p r s a m p } }$ -dilation t : $P \Theta \otimes P \Theta \ :  \ : P \Theta$ satisfying 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/2d60b6751c0d3fc05a1482cdd1decb923222c017ff0ecc051cc5325b429210c6.jpg)


(5.40) 

Indeed, one can easily check that that every $\hat { g } _ { \mathsf { p r s a m p } ^ { - } } \mathrm { d i l a t i o n }$ in $\mathsf { C } _ { P \Theta }$ is represented by a $\hat { g } _ { \mathsf { p r s a m p } }$ -dilation in C (and vice versa), so that the claim follows. 

Instantiating this in BorelStoch results in the following: A statistical experiment represented by a Markov kernel $f$ is more informative than one represented by g for every prior if and only if the resulting expected distribution over posteriors of the first experiment is more spread out than that of the second experiment for every prior, where in both parts of this statement the dependence on the prior is assumed measurable. 

## 6 Strongly Representable Markov Categories

We have seen in Section 3.3 that a.s.-compatible representability is a stronger condition on a Markov category than mere representability. In this final section, we introduce another strengthening of representability which implies a.s.-compatible representability. Although we make no further use for this notion in this paper, we believe that it may become of importance in other foundational work on probability theory and statistics in terms of Markov categories. 

Definition 6.1. Let C be a Markov category, and let f : $A \to X \otimes Y$ be any morphism for which a conditional $f _ { | X } \colon X \otimes A \to Y$ exists. Then the doubling of $f$ given X is the morphism given by 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/e26a6667425db2f5b937555a931846d315c74994478fa5cc28247b765bbb075d.jpg)


(6.1) 

We now argue that this doubling is well-defined, i.e., independent of the choice of conditional $f _ { | X }$ , using an argument which generalizes [12, Equation (12.4)]. The point is to notice that, by the definition of conditionals, the doubling of f given X can be written in several equivalent forms, 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/407055083a48d442f5c4eaf732ccea6bfb88c23e5a2fd981cc28bb6b0bf98f87.jpg)


(6.2) 

The first equation shows that the doubling is independent of the choice of the conditional on the left; and the second equation similarly shows independence of the conditional on the right. 

Of course, the doubling of f given Y is a morphism $f \otimes _ { Y } f \colon A \to X \otimes X \otimes Y$ defined similarly in terms of a conditional $f _ { | Y }$ , whenever it exists. 

Remark 6.2. For $X = I$ , the doubling of f given X is simply given by the familiar diagram 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/1ba51be1d9a9809e41d8e378270215e6dd31b5a81745a458ba08d59fffb78ca2.jpg)


(6.3) 

For $A = I$ instead, the doubling $f \otimes _ { X } f$ coincides with the conditional product of f with itself over $X$ , as introduced for Markov categories in [12, Section 13] and also denoted by $f \otimes _ { X } f$ 

Lemma 6.3. Let $f \colon A \to X \otimes Y$ be a morphism in a Markov category for which the conditional $f _ { | X }$ exists. Then the following conditions are equivalent: 

1. The doubling of f given X satisfies 

$$
\begin{array}{c c} \boxed {X Y Y} & = \\ A & \end{array} \quad \begin{array}{c c} X Y Y \\ f \otimes_ {X} f \\ A & \end{array}\tag{6.4}
$$

2. Defining 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/7f340a79b6f33a742a752ae4e5135c69572b6493f167e36af11b534d51350a3e.jpg)


(6.5) 

the conditional $f _ { | X }$ is $f _ { X } ^ { \mathrm { i c } } - a . s .$ deterministic, that is: 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/ca0d83c85ca06d795a8553b8f16166c7346231979b54c58d45792080ea8d2ffd.jpg)


(6.6) 

The second condition is independent of the choice of conditional, since a conditional $f _ { | X }$ is unique exactly up to $f _ { X } ^ { \mathrm { i c } } \mathrm { - a . s . }$ . equality, and the property of being almost surely deterministic is invariant under a.s. equality. 

Proof. Notice that substituting the definition of $f _ { X } ^ { \mathrm { i c } }$ into equation (6.6) shows that condition 2 can be rewritten as 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/d407e3247794eec119aadc8a5197d54c084653eb45ae198f431d691e80c78270.jpg)


(6.7) 

which one can recognize as equivalent to equation (6.4) if we use the definition of conditionals to simplify the right-hand side. □ 

Definition 6.4. A morphism f : $A \ \to \ X \otimes Y$ in a Markov category is termed deterministic given X if the equivalent conditions of Lemma 6.3 hold. 

The analogous property of f being deterministic given Y is then defined in terms of the doubling $f \otimes _ { Y } f$ or a conditional $f _ { | Y }$ in the obvious way. 

Remark 6.5. For $X = I$ , a morphism $f \colon A \to Y$ is deterministic given X if and only if it is deterministic. 

Remark 6.6. Here is another important special case. Let $p \colon \Theta \to A$ and $f \colon A \to Y$ be arbitrary morphisms. If f is p-a.s. deterministic, then the composite morphism 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/0471bf7def5c9014ddb88cd9f399214f8811a301489179587ce9af7af41d6ca8.jpg)


(6.8) 

is deterministic given A. Conversely, if a morphism $\Theta \to A \otimes Y$ is deterministic given A and also of the above form, then the morphism $f \colon A \to Y$ in the decomposition is $p { \mathrm { - a . s } }$ . deterministic. This follows from the second condition of Lemma 6.3 and the fact that the morphism 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/099610bd60b392baec64b8512c0f7642bac5b580a7c2884757da09246c775043.jpg)


(6.9) 

is a conditional of the one in (6.8) with respect to $A .$ . 

We write $\mathsf { C } _ { \mathrm { d e t } | X } ( A , X \otimes Y )$ for the set of morphisms $A \to X \otimes Y$ which are deterministic given X. Note that $\mathsf { C } _ { \mathrm { d e t } | X }$ by itself does not have any meaning, unlike $\mathsf { C } _ { \mathrm { d e t } }$ , which stands for the subcategory of deterministic morphisms with hom-sets $\mathsf C _ { \mathrm { d e t } } ( A , X )$ 

Here is now our notion of strong representability, which enhances the representability of Definition 3.7 by a certain kind of compatibility with the monoidal structure. 

Definition 6.7. Let C be a Markov category. Given $Y \in \mathsf { C }$ , we say that $P Y \in C$ is a strong distribution object for Y if it comes equipped with a morphism 

$$
\operatorname{samp} _ {Y} \colon P Y \to Y
$$

such that for all $A , X \in \mathsf C$ , composing with id $. x \otimes$ samp establishes a bijection 

$$
\mathsf {C} _ {\det | X} (A, X \otimes P Y) \cong \mathsf {C} (A, X \otimes Y).\tag{6.10}
$$

If a strong distribution object $P Y$ exists for every $Y _ { i }$ , then we say that the Markov category C is strongly representable. 

By Remark 6.5, taking $X = I$ shows that every strong distribution object is also a distribution object. Hence a strongly representable Markov category is in particular representable, so that the results of Section 3.2 apply, making P into a monad on $\mathsf { C } _ { \mathrm { d e t } }$ whose Kleisli category is C. 

We write $f ^ { \sharp Y } \colon A \to X \otimes P Y$ for the partial adjunct of $f \colon A \to X \otimes Y$ which is deterministic given X and satisfies 

$$
\left(\operatorname{id} _ {X} \otimes \mathsf {s a m p} _ {Y}\right) \circ f ^ {\sharp Y} = f.\tag{6.11}
$$

We similarly write $f ^ { \sharp X } \colon A \to P X \otimes Y$ for its partial adjunct which is deterministic given $Y$ 

Lemma 6.8. $I f \subset$ is a strongly representable Markov category, then for every morphism $p \colon \Theta \to A$ in C and every $X \ \in \ \mathsf C$ , composing with samp establishes a bijection between the following two sets: 

1. morphisms $A  X$ up to p-a.s. equality, 

2. p-a.s. deterministic morphisms $A \to P X$ up to p-a.s. equality. 

Proof. The first set, $\mathsf { C } ( A , X ) _ { / p - { \mathrm { a . s . } } }$ , is clearly in bijection with those morphisms in $\mathsf C ( \Theta , A \otimes X )$ which are of the form as in (6.8) with $p$ as given and $f \colon A \to X$ arbitrary. By Remark 6.6, the second set is in bijection with morphisms $\mathsf { C } _ { \mathrm { d e t } | X } ( \Theta , A \otimes P X )$ of the form as in (6.8) with $p$ fixed and $f \colon A \to P X$ being p-a.s. deterministic. 

The fact that composing with $\operatorname { i d } _ { A } \otimes \mathsf { s a m p } _ { X }$ establishes an injective function between these then follows from the fact that P X is a strong distribution object. On the other hand, the surjectivity is clear from the fact that P X is also a mere distribution object. □ 

We now investigate the relation between strong representability and a.s.- compatible representability of Markov categories. One direction is now easy. 

Corollary 6.9. A strongly representable Markov category is a.s.-compatibly representable (Definition 3.18). 

Proof. If $f , g \colon A \to P X$ are deterministic and $p { \mathrm { - a . s } }$ . equal after composing with ${ \mathsf { S a m p } } _ { X }$ , then by Lemma 6.8 it must already be the case that $f = _ { p \mathrm { - } \mathrm { a . s . } } ~ g$ □ 

By Proposition 3.21, every strongly representable Markov category therefore also satisfies the sampling cancellation property (Definition 3.20). Note that Lemma 6.8 is somewhat stronger than a.s.-compatible representability, since in particular it implies 

$$
f = _ {p \text {-a.s.}} g \qquad \Longleftrightarrow \qquad \mathsf {s a m p} f = _ {p \text {-a.s.}} \mathsf {s a m p} g\tag{6.12}
$$

as soon as $f$ and $g$ are merely $p \mathrm { - a . s . }$ . deterministic rather than actually deterministic. In the converse direction, the following result for proving that particular Markov categories are strongly representable by modularizing strong representability a bit. 

Proposition 6.10. Let C be a Markov category with conditionals. Then the following are equivalent: 

(i) C is strongly representable; 

(ii) C is a.s.-compatibly representable, and for every $f \colon A \ \to \ P X$ which is $p -$ a.s. deterministic with respect to some $p \colon \Theta \to A$ , we have 

$$
f = _ {p - a. s.} (\operatorname{samp} f) ^ {\sharp}.\tag{6.13}
$$

As one would expect, the distribution functor and sampling maps are preserved under the equivalence. 

Proof. In the forward direction, suppose that C is strongly representable. Then we have already shown that this makes C in particular a.s.-compatibly representable. The final statement involving equation (6.13) is an immediate consequence of (6.12), upon replacing $g$ by (samp $f ) ^ { \sharp }$ 

For the converse direction, we prove that a distribution object $P Y$ for any object $Y$ is also a strong distribution object for $Y$ . Thus we need to show that the map 

$$
\left(\operatorname{id} _ {X} \otimes \mathsf {s a m p} _ {Y}\right) \circ \_ \colon C _ {\det | X} (A, X \otimes P Y) \to C (A, X \otimes Y)\tag{6.14}
$$

is a bijection for all auxiliary objects A and X. To this end, we construct a map 

$$
(\underline {{\mathbf {\Phi}}}) ^ {\sharp Y} \colon \mathsf {C} (A, X \otimes Y) \to \mathsf {C} _ {\det | X} (A, X \otimes P Y)\tag{6.15}
$$

which then proves to be inverse to composition with id $x \otimes$ samp . Concretely, for any $f \colon A \to X \otimes Y$ , we define its candidate partial adjunct as 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/d08f0d6e87e77d23bf12917b19af44a5342464c5551059188f9ceb9b00bfbb63.jpg)


(6.16) 

This definition is independent of the choice of the conditional $f _ { | X }$ as a consequence of the sampling cancellation property. Furthermore, the fact that $f ^ { \sharp Y }$ is indeed deterministic given X follows directly from the fact that $( f _ { | X } ) ^ { \sharp }$ is deterministic, as in Remark 6.6. The defining property of $f _ { | X }$ as a conditional of $f$ with respect to $X$ equation (2.4), then implies that applying id $_ X \otimes \mathsf { s a m p } _ { Y }$ to $f ^ { \sharp Y }$ yields $f .$ 

In order to prove that $( \_ { \mathtt { Y } } \mathtt { Y }$ is inverse to composition with $\operatorname { i d } _ { X } \otimes \mathsf { s a m p } _ { Y }$ also in the other direction, we need to show that if $g \colon A \to X \otimes P Y$ is deterministic given $X$ , then we have 

$$
\left(\left(\operatorname{id} _ {X} \otimes \mathsf {s a m p} _ {Y}\right) g\right) ^ {\sharp Y} = g.
$$

To this end, let $g _ { \left| X \right. }$ be a conditional of $g$ with respect to $X$ . Since by Lemma 6.3 every conditional is $g _ { X } ^ { \mathrm { i c } }$ -almost surely deterministic where $g _ { X } ^ { \mathrm { i c } }$ is defined as in equation (6.5), $g _ { \left| X \right. }$ is $g _ { X } ^ { \mathrm { i c . } } - \mathrm { a . }$ s. equal to the deterministic (samp $g _ { | X } ) ^ { \sharp }$ by assumption (6.13). Therefore, (samp $g _ { | X } ) ^ { \sharp }$ is also a conditional of $g$ with respect to $X$ . We can thus assume $g _ { \left| X \right. }$ to be deterministic, which we do from now on. 

The compositionality of conditionals [12, Lemma 11.12] shows that 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/043bfd487e058670014a5a80ca048e1427c7a0cffd695aaeb302a721cbce5451.jpg)


(6.17) 

is then a conditional of 

$$
\left(\operatorname{id} _ {X} \otimes \operatorname{samp} _ {Y}\right) g = \begin{array}{c} X Y \\ \boxed {\text {samp}} \\ \boxed {g} \\ A \end{array}\tag{6.18}
$$

It follows that the deterministic morphism $g _ { \left| X \right. }$ itself is the adjunct of a conditional of $( \operatorname { i d } _ { X } \otimes \mathsf { s a m p } _ { Y } ) g$ with respect to $X$ . Thus, substituting $\left( \operatorname { i d } _ { X } \otimes \mathsf { s a m p } _ { Y } \right) g$ for $f$ in equation (6.16) results in the partial adjunct 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/c59087d2-9dc1-415a-a1ea-8d9cc590e524/5c5fe93db49d1f19136e6340b983c15716a8557e6f0ebd763347a9d440801293.jpg)


(6.19) 

as was to be shown. Consequently, $( - ) ^ { \sharp Y }$ is a two-sided inverse of $( \operatorname { i d } _ { X } \otimes \mathsf { s a m p } _ { Y } ) \circ \_$ and the proof is complete. □ 

Remark 6.11. Using the construction of $f ^ { \sharp Y }$ from $f$ as in the proof shows that the function 

$$
\left(\operatorname{id} _ {X} \otimes \operatorname{samp} _ {Y}\right) \circ \_ \colon \mathsf {C} _ {\det | X} (A, X \otimes P Y) \to \mathsf {C} (A, X \otimes Y)
$$

is surjective already as soon as $\mathsf { C }$ is representable and has conditionals, since for the surjectivity part of the proof it is irrelevant whether $f ^ { \sharp Y }$ is independent of the choice of a conditional. 

Example 6.12. We now show that BorelStoch is strongly representable by proving that the conditions of Proposition 6.10(ii) are satisfied. By Examples 2.4 and 3.19, we already know that BorelStoch has conditionals and is a.s.-compatibly representable. For the remaining condition, we prove something stronger: For any p : $A  X$ and $f \colon X \to Y$ which is $p { \mathrm { - a . s } }$ . deterministic, $f$ is p-a.s. equal to a genuinely deterministic map $X  Y$ . This then implies condition (6.13) by a.s.-compatible representability. 

First, the assumption that $f \colon X \to Y$ is $p \mathrm { - a . s . }$ . deterministic means that for every $S , T \in \Sigma _ { Y }$ , we have 

$$
f (S \cap T | x) = f (S | x) f (T | x)
$$

for $ { \boldsymbol { p } } (  { \underline { { \mathbf { \delta \pi } } } } _ { - } | a )$ -almost all $x \in X$ for all $a \in A$ . In other words, the set 

$$
N _ {S, T} := \{x \in X \mid f (S \cap T | x) \neq f (S | x) f (T | x) \}
$$

is a $p ( \_ { a } )$ -null set for all $a \in A$ . Upon choosing a generating sequence $( S _ { n } ) _ { n \in \mathbb { N } }$ in $\Sigma _ { Y } .$ , it follows that also the countable union 

$$
N := \bigcup_ {i, j} N _ {S _ {i}, S _ {j}}
$$

is $ { \boldsymbol { p } } (  { \underline { { \mathbf { \delta \pi } } } } _ { - } | a )$ -null for all $a \in \ A$ . For every element x of $X \ \backslash \ N$ , we now have $f ( S \cap T | x ) = f ( S | x ) f ( T | x )$ by the $\pi - \lambda \cdot$ -theorem. Finally, let $y \in Y$ be an arbitrary element,<sup>13</sup> and put 

$$
g (S | x) := \left\{ \begin{array}{l l} f (S | x) & \text { if } x \in X \setminus \mathcal {N} \\ \delta_ {y} (S) & \text { if } x \in \mathcal {N}. \end{array} \right.
$$

Then $g$ is deterministic by construction, and also $f = _ { p \mathrm { - } \mathrm { a . s . } } ~ g$ since $f$ and $g$ are equal by definition everywhere except on the null set $\mathcal { N }$ 

In a representable Markov category, the unit δ of the monad P satisfies naturality with respect to deterministic morphisms (Remark 3.11). In a strongly representable Markov category, this holds in the following form extended to a.s. deterministic morphisms. 

Lemma 6.13. Let C be a strongly representable Markov category and consider two morphisms $p \colon \Theta \to X$ and $f \colon X \to Y$ . If f is $p  – a . s$ . deterministic, then $\delta$ satisfies naturality with respect to f , p-almost surely: 

$$
\delta_ {Y} f = _ {p - a. s.} (P f) \circ \delta_ {X}.\tag{6.20}
$$

Proof. Since $\delta _ { Y }$ is deterministic and $f$ is $p \mathrm { - a . s . }$ . deterministic, it follows that $\delta _ { Y } f$ is also $p \mathrm { - a . s . }$ . deterministic. It is clear that the right-hand side is deterministic. Hence, by Lemma 6.8, it is enough to prove that the equation holds after composing both sides with samp . But then the left-hand side simply turns into $f ,$ as does the right-hand side, 

$$
\mathsf {s a m p} _ {Y} \circ (P f) \circ \delta_ {X} = f \circ \mathsf {s a m p} _ {X} \circ \delta_ {X} = f,\tag{6.21}
$$

by naturality of samp. 

## References



[1] Raghu Raj Bahadur. A characterization of suficiency. Ann. Math. Statist, 26(2):286–293, 1955. projecteuclid.org/euclid.aoms/1177728545. ↑ 38 





[2] David Blackwell. Comparison of experiments. In Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, pages 93–102. University of California Press, 1951. projecteuclid.org/euclid.aoms/1200500222. ↑ 5, 35, 41 





[3] David Blackwell. There are no Borel SPLIFs. Ann. Probab., 8(6):1189–1190, 1980. projecteuclid.org/euclid.aoms/1176994581. ↑ 54 





[4] David Blackwell and R. V. Ramamoorthi. A Bayes but not classically suficient statistic. Ann. Statist., 10(3):1025–1026, 1982. projecteuclid.org euclid.aos/1176345895. ↑ 53 





[5] Paul Blain Levy, John Power, and Hayo Thielecke. Modelling environments in call-by-value programming languages. Information and Computation, 185:182– 210, 2003. doi.org/10.1016/S0890-5401(03)00088-9. ↑ 4, 25 





[6] Martin Brandenburg. Tensor categorical foundations of algebraic geometry. PhD thesis, Westf¨alische Wilhelms-Universit¨at M¨unster, 2014. arXiv:1410.1716. ↑ 12, 23 





[7] Francesco Buscemi. Comparison of quantum statistical models: equivalent conditions for suficiency. Communications in Mathematical Physics, 310(3):625–647, 2012. doi.org/10.1007/s00220-012-1421-3. ↑ 6 





[8] Aurelio Carboni and Robert F. C. Walters. Cartesian bicategories. I. J. Pure Appl. Algebra, 49(1-2):11–32, 1987. core.ac.uk/download/pdf/82513341.pdf. ↑ 8 





[9] Kenta Cho and Bart Jacobs. Disintegration and Bayesian inversion via string diagrams. Math. Structures Comput. Sci., 29:938–971, 2019. arXiv:1709.00322. ↑ 3, 7, 8, 10 





[10] Dion Coumans and Bart Jacobs. Scalars, monads and categories, 2010. arXiv:1003.0585. ↑ 13 





[11] Henrique de Oliveira. Blackwell’s informativeness theorem using diagrams. Games and Economic Behavior, 109:126–131, 2018. doi.org/10.1016/j.geb. 2017.12.008. ↑ 6, 36 





[12] Tobias Fritz. A synthetic approach to Markov kernels, conditional independence and theorems on suficient statistics. Adv. Math., 370:107239, 2020. arXiv:1908.07021. ↑ 3, 7, 8, 9, 10, 12, 15, 27, 38, 39, 44, 45, 59, 64 





[13] Tobias Fritz and Paolo Perrone. Monads, partial evaluations, and rewriting. arXiv:1810.06037. To appear in Proceedings of MFPS. ↑ 32 





[14] Tobias Fritz and Paolo Perrone. Bimonoidal structure of probability monads. In Proceedings of the Thirty-Fourth Conference on the Mathematical Foundations of Programming Semantics (MFPS XXXIV), volume 341 of Electron. Notes Theor. Comput. Sci., pages 121–149. Elsevier Sci. B. V., Amsterdam, 2018. arXiv:1804.03527. ↑ 15 





[15] Tobias Fritz and Eigil Fjeldgren Rischel. The zero-one laws of Kolmogorov and Hewitt–Savage in categorical probability. Compositionality, 2:3, 2020. compositionality-journal.org/papers/compositionality-2-3. ↑ 3 





[16] Malte Gerhold, Stephanie Lachs, and Michael Sch¨urmann. Categorial L´evy processes. arXiv:1612.05139. ↑ 7 





[17] Peter V. Golubtsov. Monoidal Kleisli category as a background for information transformers theory. Информационные процессы (Information Theory and Information Processing), 2:62–84, 2002. Translated from Russian. jip.ru/ 2002/GOLU1.pdf. ↑ 3, 7, 36 





[18] Tom´aˇs Gonda and Robert W Spekkens. Monotones in general resource theories. arXiv:1912.07085. ↑ 6 





[19] Olav Kallenberg. Random measures, theory and applications, volume 77 of Probability Theory and Stochastic Modelling. Springer, Cham, 2017. ↑ 9 





[20] Gregory Maxwell Kelly. Doctrinal adjunction. In Category Seminar, volume 420 of Lecture Notes in Mathematics, pages 257–280. Springer, 1974. doi:10.1007/ BFb0063096. ↑ 21 





[21] Anders Kock. Commutative monads as a theory of distributions. Theory Appl. Categ., 26:No. 4, 97–131, 2012. arXiv:1108.5952. ↑ 12 





[22] Lucien Le Cam. Comparison of experiments: A short review. Lecture Notes–Monograph Series, pages 127–138, 1996. projecteuclid.org/euclid.lnms/ 1215453569. ↑ 36, 41, 43, 50 





[23] Arthur J. Parzygnat. Inverses, disintegrations, and Bayesian inversion in quantum Markov categories. arXiv:2001.08375. ↑ 6 





[24] Evan Patterson. The algebra and machine representation of statistical models. PhD thesis, Stanford, 2020. epatters.org/papers/#2020-thesis. ↑ 3 





[25] Paolo Perrone. Notes on category theory with examples from basic mathematics, 2019. arXiv:1912.10642. ↑ 12 





[26] Emily Riehl. Category Theory in Context. Aurora, 2016. math.jhu.edu/∼eriehl/ context.pdf. ↑ 19 





[27] Erik Torgersen. Comparison of statistical experiments, volume 36. Cambridge University Press, 1991. ↑ 38, 46 

