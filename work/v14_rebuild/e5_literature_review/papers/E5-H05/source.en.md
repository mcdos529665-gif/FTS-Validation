# Inference for the Generalization Error

CLAUDE NADEAU 

jcnadeau@altavista.net 

Health Canada, AL0900B1, Ottawa ON, Canada K1A 0L2 

YOSHUA BENGIO 

Yoshua.Bengio@umontreal.ca 

CIRANO and Dept. IRO, Université de Montréal, C.P. 6128 Succ. Centre-Ville, Montréal, Quebec, Canada H3C 3J7

Editor: Lisa Hellerstein 

Abstract. In order to compare learning algorithms, experimental results reported in the machine learning literature often use statistical tests of significance to support the claim that a new learning algorithm generalizes better. Such tests should take into account the variability due to the choice of training set and not only that due to the test examples, as is often the case. This could lead to gross underestimation of the variance of the cross-validation estimator, and to the wrong conclusion that the new algorithm is significantly better when it is not. We perform a theoretical investigation of the variance of a variant of the cross-validation estimator of the generalization error that takes into account the variability due to the randomness of the training set as well as test examples. Our analysis shows that all the variance estimators that are based only on the results of the cross-validation experiment must be biased. This analysis allows us to propose new estimators of this variance. We show, via simulations, that tests of hypothesis about the generalization error using those new variance estimators have better properties than tests involving variance estimators currently in use and listed in Dietterich (1998). In particular, the new tests have correct size and good power. That is, the new tests do not reject the null hypothesis too often when the hypothesis is true, but they tend to frequently reject the null hypothesis when the latter is false.

Keywords: generalization error, cross-validation, variance estimation, hypothesis tests, size, power 

## 1. Generalization error and its estimation

In order to compare learning algorithms, experimental results reported in the machine learning literature often use statistical tests of significance. Unfortunately, these tests often rely solely on the variability due to the test examples and do not take into account the variability due to the randomness of the training set. We perform a theoretical investigation of the variance of a cross-validation estimator of the generalization error that takes into account the variability due to the choice of training sets as well as of test examples (hold-out set). When applying a learning algorithm (or comparing several algorithms), one is typically interested in estimating its generalization error. Its estimation is rather trivial through cross-validation or the bootstrap. Providing a variance estimate of the cross-validation estimator, so that hypothesis testing and/or confidence intervals are possible, is more difficult, especially, as pointed out in Hinton et al. (1995), if one wants to take into account various sources of variability such as the choice of the training set (Breiman, 1996) or initial conditions of a learning algorithm (Kolen & Pollack, 1991). A notable effort in that direction is Dietterich’s work (Dietterich, 1998). See also the review of bounds of the accuracy of various cross-validation estimates in Devroye, Gyro¨fi, and Lugosi (1996). Building upon (Dietterich, 1998), in this paper we take into account the variability due to the choice of training sets and test examples. Specifically, an investigation of the variance to be estimated allows us to provide two new variance estimators, one of which is conservative by construction. 

The choice of estimator for the variance of an average test error (or of the difference between the average error made by two algorithms) is very important: a poor choice of estimator (especially if it is liberal, i.e., underestimates the variance) could lead to a profusion of publications in which method A is incorrectly claimed to be better than a previously proposed method B. Because of the approximately normal behavior of average error, an underestimation of the standard deviation by a factor 2, say, can yield to about 6 times more “false claims” than would have been expected for a test level of 5%. If the habit of making rigorous statistical comparisons and in particular avoiding the use of a liberal estimator is not ingrained in the machine learning community, it could be tempting for many researchers to use a liberal estimate of variance when comparing their preferred algorithm against the competition. For this reason, it is very important that reviewers insist on analyses of results that avoid liberal estimators of variance (for confidence intervals or to test the null hypothesis of method A being not better than method B). 

Let us define what we mean by “generalization error” and say how it will be estimated in this paper. We assume that data is available in the form $Z_1^n = \{Z_1, \ldots, Z_n\}$. For example, in the case of supervised learning, $Z_i = (X_i, Y_i) \in \mathcal{Z} \subseteq \mathbb{R}^{p+q}$, where $p$ and $q$ denote the dimensions of the $X_i$'s (inputs) and the $Y_i$'s (outputs). We also assume that the $Z_i$'s are independent with $Z_i \sim P(Z)$, where the generating distribution $P$ is unknown. Let $\mathcal{L}(D;Z)$, where $D$ represents a subset of size $n_1 \leq n$ taken from $Z_1^n$, be a function from $\mathcal{Z}^{n_1} \times \mathcal{Z}$ to $\mathbb{R}$. For instance, this function could be the loss incurred by the decision that a learning algorithm trained on $D$ makes on a new example $Z$.

We are interested in estimating ${}_{n}\mu \equiv E [ \mathcal { L } ( Z _ { 1 } ^ { n } ; Z _ { n + 1 } ) ]$ where $Z _ { n + 1 } \sim P ( Z )$ is independent of $Z _ { 1 } ^ { n }$ . The subscript stands for the size of the training set $n$ $( Z _ { 1 } ^ { n }$ here). Note that the above expectation is taken over $Z _ { 1 } ^ { n }$ and $Z _ { n + 1 }$ , meaning that we are interested in the performance of an algorithm rather than the performance of the specific decision function it yields on the data at hand. Dietterich (1998) has introduced a taxonomy of statistical questions in Machine Learning, which we briefly summarize here. At the top level is whether the questions refer to single or multiple domains (type 9). For single domains, Dietterich distinguishes between the analysis of a single (given or already trained) predictor (types 1 through 4) and the analysis of a learning algorithm that can yield such predictors given a training set (types 5 through 8). For the former, the training set is considered fixed, whereas for the latter the training set is considered to be random. In this paper, we are concerned with the analysis of the performance of learning algorithms (types 5 through 8), not of particular trained predictors. Dietterich further splits types 5 through 8 according to whether the sample size is large or not and whether one is interested in the generalization error of a single algorithm or wants to compare the generalization errors of various algorithms. 

Let us now introduce some notation and definitions. We shall call ${ } _ { n } \mu$ the generalization error even though it can go beyond that as we now illustrate. Here are two examples. 

- Generalization error. We may take as our basic measurement 

$$
\mathcal {L} (D; Z) = \mathcal {L} (D; (X, Y)) = Q (F (D) (X), Y),\tag{1}
$$

where F represents a learning algorithm that yields a function $f = F ( D ) \ ( F ( D )$ $\mathbb { R } ^ { p } \to \mathbb { R } ^ { q } )$ , when training the algorithm on D, and Q is a loss function measuring the inaccuracy of a decision $f ( X )$ when Y is observed. For instance, for classification problems, we could have 

$$
Q (\hat {y}, y) = I [ \hat {y} \neq y ],\tag{2}
$$

where I [ ] is the indicator function, and in the case of regression, 

$$
Q (\hat {y}, y) = \| \hat {y} - y \| ^ {2},\tag{3}
$$

where $\| \cdot \|$ is the Euclidean norm. In that case ${}_{n}\mu = E [ \mathcal L ( Z _ { 1 } ^ { n } , Z _ { n + 1 } ) ]$ is the generalization error of algorithm $F$ on data sampled from $P$ . 

- Comparison of generalization errors. Sometimes, what we are interested in is not the performance of algorithms per se, but how two algorithms compare with each other. In that case we may want to consider 

$$
\mathcal {L} (D; Z) = \mathcal {L} (D; (X, Y)) = Q (F _ {A} (D) (X), Y) - Q (F _ {B} (D) (X), Y),\tag{4}
$$

where $F _ { A } ( D )$ and $F _ { B } ( D )$ are decision functions obtained when training two algorithms (respectively A and B) on $D ,$ and $Q$ is a loss function. In this case ${ } _ { n } \mu$ would be a difference of generalization errors. 

The generalization error is often estimated via some form of cross-validation. Since there are various versions of the latter, we lay out the specific form we use in this paper. 

- Let $S _ { j }$ be a random set of $n _ { 1 }$ distinct integers from $\{ 1 , \dots , n \} ( n _ { 1 } < n )$ . Here $n _ { 1 }$ is not random and represents the size of a training set. We shall let $n _ { 2 } = n - n _ { 1 }$ be the size of the corresponding test set (or hold-out set). 

- Let $S_1, \dots, S_J$ be such random index sets (of size $n_1$), sampled independently of each other, and let $S_j^c = \{1, \ldots, n\} \setminus S_j$ denote the complement of $S_j$.

- Let $Z_{S_j} = \{Z_i \mid i \in S_j\}$ be the training set obtained by subsampling $Z_1^n$ according to the random index set $S_j$. The corresponding test set (or hold-out set) is $Z_{S_j^c} = \{Z_i \mid i \in S_j^c\}$.

- Let $L(j,i) = \mathcal{L}(Z_{S_j};Z_i)$. According to (1), this could be the error an algorithm trained on the training set $Z_{S_j}$ makes on example $Z_i$. According to (4), this could be the difference of such errors for two different algorithms.

- Let $\hat{\mu}_j = \frac{1}{n_2}\sum_{i\in S_j^c}L(j,i)$ denote the usual “average test error” measured on the test set $Z_{S_j^c}$.

Then the cross-validation estimate of the generalization error considered in this paper is 

$$
{}_{n_1}^{n_2}\hat{\mu}_J = \frac{1}{J}\sum_{j=1}^{J}\hat{\mu}_j.\tag{5}
$$

Note that this an unbiased estimator of $_ { n _ { 1 } } \mu = E [ \mathcal { L } ( Z _ { 1 } ^ { n _ { 1 } } , Z _ { n + 1 } ) ]$ , which is not quite the same as ${ } _ { n } \mu$ 

This paper is about the estimation of the variance of the above cross-validation estimator. There are many variants of cross-validation, and the above variant is close to the popular K -fold cross-validation estimator, which has been found more reliable than the leave-one-out estimator (Kohavi, 1995). It should be noted that our goal in this paper is not to compare algorithms in order to perform model selection (i.e., to choose exactly one among several learning algorithms for a particular task, given a data set on which to train them). The use of cross-validation estimators for model selection has sparked a debate in the last few years (Zhu & Rohwer, 1996; Goutte, 1997) related to the “no free lunch theorem” (Wolpert & Macready, 1995), since cross-validation model selection often works well in practice but it is probably not a universally good procedure. 

This paper does not address the issue of model selection but rather that of estimating the uncertainty in a cross-validation type of estimator for generalization error, namely ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ For this purpose, this paper studies estimators of the variance of $^ { n _ { 2 } } _ { n _ { 1 } } \hat { \mu } _ { J }$ (in the sense that different values of $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ would have been obtained if a different data set $Z _ { 1 } ^ { n }$ had been sampled from the same unknown underlying distribution P and different random index sets $\vec { S _ { j } \ \mathrm { { s } } }$ had been generated). The application of the estimators studied in this paper may be for example (1) to provide confidence intervals around estimated generalization error, or (2) to perform a hypothesis test in order to determine whether an algorithm’s estimated performance is significantly above or below the performance of another algorithm. The latter is very important when researchers introduce a new learning algorithm and they want to show that it brings a significant improvement with respect to previously known algorithms. 

We first study theoretically the variance of ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ in Section 2. This will lead us to two new variance estimators we develop in Section 3. Section 4 shows how to test hypotheses or construct confidence intervals. Section 5 describes a simulation study we performed to see how the proposed statistics behave compared to statistics already in use. Section 6 concludes the paper. Before proceeding with the rest of the paper, some readers may prefer to read Appendix A.0 that presents some statistical prerequisites relevant to the rest of the paper. 

## 2. Analysis of Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$

In this section, we study Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ and discuss the difficulty of estimating it. This section is important as it enables us to understand why some inference procedures about ${ } _ { n _ { 1 } } \mu$ presently in use are inadequate, as we shall underline in Section 4. This investigation also enables us to develop estimators of $\operatorname{Var} [ { } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ in Section 3. Before we proceed, we state a lemma that will prove useful in this section, and later ones as well. 

Lemma 1. Let $U _ { 1 } , \dots , U _ { K }$ be random variables with common mean $\beta$ and the following covariance structure 

$$
\operatorname{Var} \left[ U _ {k} \right] = \delta , \quad \forall k \quad \operatorname{Cov} \left[ U _ {k}, U _ {k ^ {\prime}} \right] = \gamma , \quad \forall k \neq k ^ {\prime}.
$$

Let $\pi = \gamma/\delta$ be the correlation between $U_k$ and $U_{k'}$ ($k \ne k'$). Let $\bar{U} = K^{-1}\sum_{k=1}^{K}U_k$ and $S_U^2 = \frac{1}{K-1}\sum_{k=1}^{K}(U_k-\bar{U})^2$ be the sample mean and sample variance respectively. Then

1. $\operatorname{Var}[\bar{U}] = \gamma + \frac{\delta-\gamma}{K} = \delta\left(\pi+\frac{1-\pi}{K}\right)$.

2. If the stated covariance structure holds for all $K$ (with $\gamma$ and $\delta$ not depending on $K$), then $\gamma \geq 0$ and

$\lim_{K\to\infty}\operatorname{Var}[\bar{U}] = 0 \Leftrightarrow \gamma = 0$.

3. $E[S_U^2] = \delta - \gamma$.

**Proof.**

1. This result is obtained from a standard development of $\operatorname{Var} [ \bar { U } ]$ 

2. If $\gamma \ < 0$ , then $\operatorname{Var} [ \bar { U } ]$ would eventually become negative as K is increased. We thus conclude that $\gamma \geq 0$ . From item 1, it is obvious that $\operatorname{Var} [ \bar { U } ]$ goes to zero as K goes to infinity if and only if $\gamma = 0$ 

3. Again, this only requires careful development of the expectation. The task is somewhat easier if one uses the identity 

$$
S _ {U} ^ {2} = \frac {1}{K - 1} \sum_ {k = 1} ^ {K} \left(U _ {k} ^ {2} - \bar {U} ^ {2}\right) = \frac {1}{2 K (K - 1)} \sum_ {k = 1} ^ {K} \sum_ {k ^ {\prime} = 1} ^ {K} \left(U _ {k} - U _ {k ^ {\prime}}\right) ^ {2}.
$$

Although we only need it in Section 4, it is natural to introduce a second lemma here as it is a continuation of Lemma 1. 

Lemma 2. Let $U _ { 1 } , \dots , U _ { K } , U _ { K + 1 }$ be random variables with mean, variance and covariance as described in Lemma 1. In addition, assume that the vector $( U _ { 1 } , \dots , U _ { K } , U _ { K + 1 } )$ follows the multivariate Gaussian distribution. Again, let $\begin{array} { r } { \bar { U } = K ^ { - 1 } \sum _ { k = 1 } ^ { K } U _ { k } } \end{array}$ and $\begin{array} { r } { S_U^2 = \frac { 1 } { K - 1 } \sum _ { k = 1 } ^ { K } ( U _ { k } - \bar { U } ) ^ { 2 } } \end{array}$ be respectively the sample mean and sample variance of $U _ { 1 } , \dots , U _ { K }$ . Then 

$$
1. \sqrt {1 - \pi} \frac {U _ {K + 1} - \beta}{\sqrt {S _ {U} ^ {2}}} \sim t _ {K - 1},
$$

2. $\begin{array} { r } { \sqrt { \frac { 1 - \pi } { 1 + ( K - 1 ) \pi } } \frac { \sqrt { K } ( \bar { U } - \beta ) } { \sqrt { S_U ^ { 2 } } } \sim t _ { K - 1 } . } \end{array}$ 

where $\begin{array} { r } { \pi = \frac { \gamma } { \delta } } \end{array}$ as in Lemma 1, and $t _ { K - 1 }$ refers to Student’s t distribution with $( K - 1 )$ degrees of freedom. 

**Proof.** See Appendix A.1.

To study Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ we need to define the following covariances. In the following, $S _ { j }$ and $S _ { j ^ { \prime } }$ are independent random index sets, each consisting of $n _ { 1 }$ distinct integers from $\{ 1 , \ldots , n \}$ . Also, expectations are totally unconditional, that is expectations (as well as variances and covariances) are taken over $Z _ { 1 } ^ { n } , S _ { j } , S _ { j ^ { \prime } } , i$ and $i ^ { \prime } .$ . 

- Let $\sigma _ { 0 } = \sigma _ { 0 } ( n _ { 1 } ) = \operatorname{Var} [ L ( j , i ) ]$ when i is randomly drawn from $S _ { j } ^ { c } .$ . To establish that $\sigma _ { 0 }$ does not depend on n we note that Var[ $L ( j , i ) ] = E _ { S _ { j } , i } [ \operatorname{Var} _ { Z _ { 1 } ^ { n } } [ \mathcal { \bar { L } } ( Z _ { S _ { j } } ; Z _ { i } ) \mid S _ { j } , i ] ] +$ $\operatorname{Var} _ { S _ { j } , i } [ E _ { Z _ { 1 } ^ { n } } [ \mathcal { L } ( Z _ { S _ { j } } ; Z _ { i } ) \mid S _ { j } , i ] ]$ . Now the distribution of $\mathcal { L } ( Z _ { S _ { j } } ; Z _ { i } )$ does not depend on the particular realization of $S _ { j }$ and $i ,$ it is just the distribution of $\mathcal { L } ( Z _ { 1 } ^ { n _ { 1 } } ; Z _ { n _ { 1 } + 1 } )$ . Thus $\sigma _ { 0 } = E _ { S _ { j } , i } [ \operatorname{Var} [ \mathcal { L } ( Z _ { 1 } ^ { n _ { 1 } } ; Z _ { n _ { 1 } + 1 } ) ] ] + \operatorname{Var} _ { S _ { j } , i } [ \mathbf { \Phi } _ { n _ { 1 } } \mu ] = \operatorname{Var} [ \mathcal { L } ( Z _ { 1 } ^ { n _ { 1 } } ; Z _ { n _ { 1 } + 1 } ) ]$ depends only on $n _ { 1 } .$ , not on n . 

- Let $\sigma _ { 1 } = \sigma _ { 1 } ( n _ { 1 } , n _ { 2 } ) = \operatorname{Var} [ \hat { \mu } _ { j } ] .$ 

- Let $\sigma _ { 2 } = \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } ) = \operatorname{Cov} [ L ( j , i ) , L ( j ^ { \prime } , i ^ { \prime } ) ]$ , with $j \neq j ^ { \prime } , i$ and $i ^ { \prime }$ randomly and independently drawn from $S _ { j } ^ { c }$ and $S _ { j ^ { \prime } } ^ { c }$ respectively. 

- Let $\sigma _ { 3 } = \sigma _ { 3 } ( n _ { 1 } ) = \operatorname{Cov} [ L ( j , i ) , L ( j , i ^ { \prime } ) ]$ for $i , i ^ { \prime } \in S _ { j } ^ { c }$ and $i \neq i ^ { \prime }$ , that is i and $i ^ { \prime }$ are sampled without replacement from $S _ { j } ^ { c }$ . Using a similar argument as for $\sigma _ { 0 }$ allows one to show that $\sigma _ { 3 }$ does not depend on $n _ { 2 }$ 

Let us look at the mean and variance of ${ \hat { \mu } } _ { j } \ ( \mathrm { i . e . }$ , over one set) and ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } \ ( \mathrm { i . e . }$ , over J sets). Concerning expectations, we obviously have $E [ \hat { \mu } _ { j } ] = {}_{n_1}\mu$ and thus $E[{}_{n_1}^{n_2}\hat{\mu}_J] = {}_{n_1}\mu.$ From Lemma 1, we have 

$$
\sigma_ {1} = \sigma_ {1} (n _ {1}, n _ {2}) = \mathrm{Var} [ \hat {\mu} _ {j} ] = \sigma_ {3} + \frac {\sigma_ {0} - \sigma_ {3}}{n _ {2}} = \frac {(n _ {2} - 1) \sigma_ {3} + \sigma_ {0}}{n _ {2}}.\tag{6}
$$

For $j \neq j ^ { \prime }$ , we have 

$$
\operatorname{Cov} \left[ \hat {\mu} _ {j}, \hat {\mu} _ {j ^ {\prime}} \right] = \frac {1}{n _ {2} ^ {2}} \sum_ {i \in S _ {j} ^ {c}} \sum_ {i ^ {\prime} \in S _ {j ^ {\prime}} ^ {c}} \operatorname{Cov} \left[ L (j, i), L \left(j ^ {\prime}, i ^ {\prime}\right) \right] = \sigma_ {2},\tag{7}
$$

and therefore (using Lemma 1 again) 

$$
\operatorname{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right] = \sigma_ {2} + \frac {\sigma_ {1} - \sigma_ {2}}{J} = \sigma_ {1} \left(\rho + \frac {1 - \rho}{J}\right) = \sigma_ {2} + \frac {\sigma_ {3} - \sigma_ {2}}{J} + \frac {\sigma_ {0} - \sigma_ {3}}{n _ {2} J},\tag{8}
$$

where $\begin{array} { r } { \rho = \frac { \sigma _ { 2 } } { \sigma _ { 1 } } = \operatorname{corr} [ \hat { \mu } _ { j } , \hat { \mu } _ { j { ' } } ] } \end{array}$ . Asking how to choose J amounts to asking how large is $\rho .$ If it is large, then taking $J > 1$ (rather than $J = 1 )$ does not provide much improvement in the estimation of $n _ { 1 } \mu$ . We provide some guidance on the choice of J in Section 5. 

Equation (8) lends itself to an interesting interpretation. First we get that $\sigma _ { 2 } = \operatorname{Var} [ {}_{n_1}^{n_2} \hat { \mu } _ { \infty } ]$ with 

$$
{ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty } = \lim _ { J \to \infty } { } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } = \lim _ { J \to \infty } \frac { 1 } { J } \sum _ { j = 1 } ^ { J } \hat { \mu } _ { j } = \frac { 1 } { \binom { n } { n _ { 1 } } n _ { 2 } } \sum _ { s \in C ( \{ 1 , \dots , n \} , n _ { 1 } ) } \sum _ { i \in \{ 1 , \dots , n \} \setminus s } \mathcal { L } ( Z _ { s } ; Z _ { i } ) ,
$$

where $C ( \{ 1 , \dots , n \} , n _ { 1 } )$ , as defined in Appendix $\mathbf { A . } 2 .$ , is the set of all possible subsets of $n _ { 1 }$ distinct integers from $\{ 1 , \ldots , n \}$ . We justify the last equality as follows. What happens when J goes to infinity is that all possible errors (there are $( \mathbf { \Phi } _ { n _ { 1 } } ^ { n } ) n _ { 2 }$ different ways to choose a training set and a test example) appear with relative frequency $\overset { 1 } { ( { \underset { n _ { 1 } } { n } } ) n _ { 2 } }$ . In other words, $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty }$ is like ${ } _ { n _ { 1 } } ^ { n _ { 2 } } { \hat { \mu } } .$ <sub>J</sub> except that all $\textstyle { \binom { n } { n _ { 1 } } }$ possible training sets are chosen exactly once. Briefly, sampling infinitely often with replacement is equivalent to sampling exhaustively without replacement (i.e. a census). We also have $\mathbf { \Sigma } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty } = E _ { S _ { j } } [ \hat { \mu } _ { j } \mid Z _ { 1 } ^ { n } ] \forall j$ and therefore ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty } = E [ { } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } \mid Z _ { 1 } ^ { n } ]$ Thus $\sigma _ { 2 } = \operatorname{Var} [ E [ { \underset { n _ { 1 } } { \overset { n _ { 2 } } { n _ { 2 } } } } { \hat { \mu } } _ { J } \ | \ Z _ { 1 } ^ { n } ] ]$ so that we must have E[Var[ $\begin{array} { r } { { \bf \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } \mid Z _ { 1 } ^ { n } ] \mid = { \frac { \sigma _ { 1 } - \sigma _ { 2 } } { J } } } \end{array}$ 

We shall often encounter $\sigma _ { 0 } , \sigma _ { 1 } , \sigma _ { 2 }$ and $\sigma _ { 3 }$ in the future, so some knowledge about those quantities is valuable. Here’s what we can say about them. 

Proposition 1. For given $n _ { 1 }$ and $n _ { 2 }$ , we have $0 \leq \sigma _ { 2 } \leq \sigma _ { 1 } \leq \sigma _ { 0 }$ and $0 \le \sigma _ { 3 } \le \sigma _ { 1 }$ 

Proof: For $j \neq j ^ { \prime }$ we have 

$$
\sigma_ {2} = \operatorname{Cov} [ \hat {\mu} _ {j}, \hat {\mu} _ {j ^ {\prime}} ] \leq \sqrt {\operatorname{Var} [ \hat {\mu} _ {j} ] \operatorname{Var} [ \hat {\mu} _ {j ^ {\prime}} ]} = \sigma_ {1}.
$$

Since $\sigma_0 = \operatorname{Var}[L(j,i)]$, $i\in S_j^c$, and $\hat{\mu}_j$ is the mean of the $L(j,i)$'s, then $\sigma_1 = \operatorname{Var}[\hat{\mu}_j] \leq \operatorname{Var}[L(j,i)] = \sigma_0$. The fact that $\lim_{J\to\infty}\operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J] = \sigma_2$ provides the inequality $0\leq\sigma_2$. Regarding $\sigma_3$, we deduce $\sigma_3\leq\sigma_1$ from (6), while $0\leq\sigma_3$ is derived from the fact that $\lim_{n_2\to\infty}\operatorname{Var}[\hat{\mu}_j]=\sigma_3$. □

Naturally the inequalities are strict provided $L ( j , i )$ is not perfectly correlated with $L ( j , i ^ { \prime } ) , \hat { \mu } _ { j }$ is not perfectly correlated with $\hat { \mu } _ { j ^ { \prime } }$ , and the variances used in the proof are positive. 

A natural question about the estimator ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ is how $n _ { 1 } , n _ { 2 }$ and J affect its variance. 

Proposition 2. The variance of ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ is non-increasing in J and $n _ { 2 }$ . 

Proof: 

- Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ is non-increasing (decreasing actually, unless $\sigma _ { 1 } = \sigma _ { 2 } )$ in J as obviously seen from $( 8 )$ . This means that averaging over many train/test improves the estimation of $n _ { 1 } \mu$ • From (8), we see that to show that Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ is non-increasing in $n _ { 2 }$ , it is sufficient to show that $\sigma _ { 1 }$ and $\sigma _ { 2 }$ are non-increasing in $n _ { 2 }$ . For $\sigma _ { 1 } .$ , this follows from (6) and Proposition 1. Regarding $\sigma _ { 2 } .$ we show in Appendix $\mathrm { A } . 2$ that it is non-increasing in $n _ { 2 } . ~ \text{All}$ this to say that for a given $n _ { 1 }$ , the larger the test set size, the better the estimation of $n _ { 1 } \mu$ □ 

The behavior of $\operatorname{Var} [ { } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ with respect to $n _ { 1 }$ is unclear, but we conjecture as follows. 

Conjecture 1. In most situations, Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ should decrease in $n _ { 1 }$ . 

Argument.<sup>1</sup> The variability in ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ comes from two sources: sampling decision rules (training process) and sampling testing examples. Holding $n _ { 2 }$ and J fixed freezes the second source of variation as it solely depends on those two quantities, not $n _ { 1 }$ . The problem to solve becomes: how does $n _ { 1 }$ affect the first source of variation? It is not unreasonable to expect that the decision function yielded by a “stable” learning algorithm is less variable when the training set is larger. See Kearns and Ron (1997) showing that for a large class of algorithms including those minimizing training error, cross-validation estimators are not much worse than the training error estimator (which itself improves in $O ( V C \mathrm{dim} / n _ { 1 } )$ as the size of the training set increases (Vapnik, 1982)). Therefore we conclude that, for many cases of interest, the first source of variation, and thus the total variation (that is Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } J ] )$ is decreasing in $n _ { 1 }$ 

Regarding the estimation of Var[ $^ { n _ { 2 } } _ { n _ { 1 } } \hat { \mu } _ { J } ]$ , we show below that we can easily estimate unbiasedly $( \sigma _ { 1 } - \sigma _ { 2 } ) , ( \sigma _ { 0 } - \sigma _ { 3 } )$ and $( \sigma _ { 2 } + ( \mathbf { \sigma } _ { n _ { 1 } } \mu ) ^ { 2 } )$ . 

- From Lemma 1, we obtain readily that the sample variance of the $\hat { \mu } _ { j } { \bf \ ' } _ { \bf S }$ (call it $S _ { \hat { \mu } _ { j } } ^ { 2 }$ as in Eq. (9)) is an unbiased estimate of $\begin{array} { r } { \sigma _ { 1 } - \sigma _ { 2 } = \sigma _ { 3 } - \sigma _ { 2 } + \frac { \sigma _ { 0 } - \sigma _ { 3 } } { n_2 } } \end{array}$ . Let us interpret this result. Given $Z _ { 1 } ^ { n }$ , the $\hat { \mu } _ { j } \mathrm { ' s }$ are J independent draws (with replacement) from a hat containing all $\textstyle { \left( \begin{array} { l } { n } \\ { n _ { 1 } } \end{array} \right) }$ possible values of the $\hat { \mu } _ { j } \mathrm { ' s }$ . The sample variance of those J observations $( S _ { \hat { \mu } _ { j } } ^ { 2 } )$ is therefore an unbiased estimator of the variance of $\hat { \mu } _ { j } ,$ , given $Z _ { 1 } ^ { n }$ , i.e. an unbiased estimator of $\operatorname{Var} [ \hat { \mu } _ { j } \mid Z _ { 1 } ^ { n } ]$ , not $\operatorname{Var} [ \hat { \mu } _ { j } ]$ . This permits an alternative derivation of the expectation of the sample variance. Indeed, we have 

$$
\begin{array}{c} E _ {Z _ {1} ^ {n}, S.} \big [ S _ {\hat {\mu} _ {j}} ^ {2} \big ] = E _ {Z _ {1} ^ {n}} \big [ E _ {S.} \big [ S _ {\hat {\mu} _ {j}} ^ {2} \mid Z _ {1} ^ {n} \big ] \big ] = E _ {Z _ {1} ^ {n}} \big [ \mathrm{Var} _ {S _ {j}} \big [ \hat {\mu} _ {j} \mid Z _ {1} ^ {n} \big ] \big ] \\ = \mathrm{Var} _ {Z _ {1} ^ {n}, S _ {j}} [ \hat {\mu} _ {j} ] - \mathrm{Var} _ {Z _ {1} ^ {n}} \big [ E _ {S _ {j}} \big [ \hat {\mu} _ {j} \mid Z _ {1} ^ {n} \big ] \big ] = \sigma_ {1} - \mathrm{Var} _ {Z _ {1} ^ {n}} \big [   n _ {2}   \hat {\mu} _ {\infty}   \big ] = \sigma_ {1} - \sigma_ {2}, \end{array}
$$

where S<sub>.</sub> denotes the random index sets $( S _ { 1 } , \ldots , S _ { J } )$ . Note that $E [ \hat { \mu } _ { j } \mid Z _ { 1 } ^ { n } ] = { } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty }$ and Var[ $\mathbf { \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty } ] = \sigma _ { 2 }$ both come from the discussion after $\operatorname { E q . } \left( 8 \right)$ 

- For a given $j$ , the sample variance of the $L ( j , i ) ^ { \prime } \mathrm { s } ( i \in S_j^c )$ is unbiased for $\sigma _ { 0 } - \sigma _ { 3 }$ according to Lemma 1 again. We may average these sample variances over $j$ to obtain a more accurate estimate of $\sigma _ { 0 } - \sigma _ { 3 }$ 

- From Eq. (7) we have $E [ \hat { \mu } _ { j } \hat { \mu } _ { j ^ { \prime } } ] = \sigma _ { 2 } + ( \mathbf { \mu } _ { n _ { 1 } } \mu ) ^ { 2 }$ for $j \neq j ^ { \prime }$ , so the sample average of the $\hat { \mu } _ { j } \hat { \mu } _ { j { ' } }$ will be unbiased for $( \sigma _ { 2 } + ( \mathbf { \sigma } _ { n _ { 1 } } \mu ) ^ { 2 } )$ 

Since we can estimate $( \sigma _ { 1 } - \sigma _ { 2 } ) , ( \sigma _ { 0 } - \sigma _ { 3 } )$ and $( \sigma _ { 2 } + { \textstyle \binom { } { n _ { 1 } } } \mu ) ^ { 2 } )$ without bias, we are thus able to estimate unbiasedly any linear combination of $( \sigma _ { 0 } - \sigma _ { 3 } ) , ( \sigma _ { 3 } - \sigma _ { 2 } )$ and $( \sigma _ { 2 } + { \binom { } { n _ { 1 } } } \mu ) ^ { 2 } )$ . This is not sufficient to unbiasedly estimate Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ shown in (8). We now tackle the question of whether or not there exists an unbiased estimator of Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ . Potential estimators may be put in two classes: (i) those that are linear and/or quadratic in the $L ( j , i ) ^ { \prime } \mathrm { s } , \mathrm { ( i i ) }$ those that are not. Because of the general framework of the paper, it is impossible to say anything about the distribution of the $L(j,i)$'s beyond their means and covariances (to say anything more requires assumptions about the distribution of $Z _ { 1 } ^ { n }$ , the learning algorithms and the loss function $\mathcal { L } )$ . Hence we are only able to derive mathematical expectations for estimators within class (i). We obviously cannot identify an unbiased estimator of Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } J ]$ in class (ii) since we cannot derive expectations in this class. The following proposition shows that there is no unbiased estimator of Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } J ]$ in class (i). 

Proposition 3. There is no general unbiased estimator of Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ that involves the $L ( j , i ) ^ { \prime } s$ in a quadratic and/or linear way. 

Proof: Let $\vec { L } _ { j }$ be the vector of the $L(j,i)$'s involved in $\hat { \mu } _ { j }$ and $\vec { L }$ be the vector obtained by concatenating the $\vec { L } _ { j } \mathrm { ' s } ; \vec { L }$ is thus a vector of length $n _ { 2 } J$ . We know that $\vec { L }$ has expectation ${ \bf \Pi } _ { n _ { 1 } } \mu { \bf 1 } _ { n _ { 2 } J }$ and variance 

$$
\operatorname{Var} [ \vec {L} ] = \sigma_ {2} \mathbf {1} _ {n _ {2} J} \mathbf {1} _ {n _ {2} J} ^ {\prime} + (\sigma_ {3} - \sigma_ {2}) I _ {J} \otimes \left(\mathbf {1} _ {n _ {2}} \mathbf {1} _ {n _ {2}} ^ {\prime}\right) + (\sigma_ {0} - \sigma_ {3}) I _ {n _ {2} J},
$$

where $I _ { k }$ is the identity matrix of order $k , \mathbf { 1 } _ { k }$ is the $k \times 1$ vector filled with $1 \mathrm { { } } \mathrm { { \dot { s } } }$ and $\otimes$ denotes Kronecker’s product. We consider estimators of Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } J ]$ of the following form 

$$
\hat {V} \big [ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \big ] = \vec {L} ^ {\prime} A \vec {L} + b ^ {\prime} \vec {L}
$$

Using the fact that $\begin{array} { r } { { \bf 1 } _ { n _ { 2 } J } ^ { \prime } A { \bf 1 } _ { n _ { 2 } J } = \operatorname{trace} ( A { \bf 1 } _ { n _ { 2 } J } { \bf 1 } _ { n _ { 2 } J } ^ { \prime } ) } \end{array}$ , we have 

$$
\begin{array}{l} E \big [ \hat {V} \big [ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \big ] \big ] = \operatorname{trace} (A \operatorname{Var} [ \vec {L} ]) + E [ \vec {L} ] ^ {\prime} A E [ \vec {L} ] + b ^ {\prime} E [ \vec {L} ] \\ \qquad = (\sigma_ {3} - \sigma_ {2}) \operatorname{trace} \big (A \big (I _ {J} \otimes \big (\mathbf {1} _ {n _ {2}} \mathbf {1} _ {n _ {2}} ^ {\prime} \big) \big) \big) + (\sigma_ {0} - \sigma_ {3}) \operatorname{trace} (A) \\ \qquad + \big (\sigma_ {2} + \mathbf {\Sigma} _ {n _ {1}} \mu^ {2} \big) \mathbf {1} _ {n _ {2} J} ^ {\prime} A \mathbf {1} _ {n _ {2} J} + \mathbf {\Sigma} _ {n _ {1}} \mu b ^ {\prime} \mathbf {1} _ {n _ {2} J}. \end{array}
$$

Since we wish $\hat { V } \big [ \mathbf { \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } \big ]$ to be unbiased for Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ , we want $0 = b ^ { \prime } \mathbf { 1 } _ { n _ { 2 } J } = \mathbf { 1 } _ { n , J } ^ { \prime } A \mathbf { 1 } _ { n _ { 2 } J }$ to get rid of $n _ { 1 } \mu$ in the above expectation. Once those restrictions are incorporated into $\hat { V } [ { \bf \Xi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ] .$ , we have 

$$
E \left[ \hat {V} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right] \right] = (\sigma_ {3} - \sigma_ {2}) \operatorname{trace} \left(A \left(I _ {J} \otimes \left(\mathbf {1} _ {n _ {2}} \mathbf {1} _ {n _ {2}} ^ {\prime}\right)\right)\right) + (\sigma_ {0} - \sigma_ {3}) \operatorname{trace} (A).
$$

Since Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ is not a linear combination of $( \sigma _ { 3 } - \sigma _ { 2 } )$ and $( \sigma _ { 0 } - \sigma _ { 3 } )$ alone, we conclude that $\hat { V } \big [ \mathbf { \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } \big ]$ cannot be unbiased for Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ in general. □ 

## 3. Estimation of $\operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$

We are interested in estimating ${}_{n_1}^{n_2}\sigma_J^2 = \operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$, where ${}_{n_1}^{n_2}\hat{\mu}_J$ is as defined in (5). We provide two new estimators of $\operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$ that shall be compared, in Section 5, to estimators currently in use and presented in Section 4. The first estimator is simple but may have a positive or negative bias for the actual variance. The second estimator is meant to lead to conservative inference (see Appendix A); that is, if Conjecture 1 is correct, its expected value exceeds the actual variance.

## 3.1. First method: Approximating ρ

Let us recall from (5) that $\begin{array} { r } { { \bf \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } = \frac { 1 } { J } \sum _ { j = 1 } ^ { J } \hat { \mu } _ { j } } \end{array}$ . Let 

$$
S _ {\hat {\mu} _ {j}} ^ {2} = \frac {1}{J - 1} \sum_ {j = 1} ^ {J} \left(\hat {\mu} _ {j} - \mathbf {\Pi} _ {n _ {1}} ^ {n _ {2}} \hat {\mu} _ {J}\right) ^ {2}\tag{9}
$$

be the sample variance of the $\boldsymbol { \hat { \mu } _ { j } } \mathrm { \bf { s } . }$ . According to Lemma 1, 

$$
\begin{array}{c} E \Big [ S _ {\hat {\mu} _ {j}} ^ {2} \Big ] = \sigma_ {1} (1 - \rho) = \frac {1 - \rho}{\rho + \frac {1 - \rho}{J}} \sigma_ {1} \left(\rho + \frac {1 - \rho}{J}\right) \\ = \frac {\sigma_ {1} \left(\rho + \frac {1 - \rho}{J}\right)}{\frac {1}{J} + \frac {\rho}{1 - \rho}} = \frac {\mathrm{Var} \big [ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \big ]}{\frac {1}{J} + \frac {\rho}{1 - \rho}}, \end{array}\tag{10}
$$

so that $\left(\frac{1}{J}+\frac{\rho}{1-\rho}\right)S_{\hat{\mu}_j}^2$ is an unbiased estimator of $\operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$. The only problem is that $\rho=\rho(n_1,n_2)=\sigma_2(n_1,n_2)/\sigma_1(n_1,n_2)$, the correlation between the $\hat{\mu}_j$'s, is unknown and difficult to estimate. Indeed, neither $\sigma_1$ nor $\sigma_2$ can be written as a linear combination of ${}_{n_1}\mu$, $\sigma_2+({}_{n_1}\mu)^2$, $\sigma_0-\sigma_3$, and $\sigma_3-\sigma_2$, the quantities we know how to estimate unbiasedly (besides their linear combinations). We use a very naive surrogate for $\rho$ as follows. Recall that $\hat{\mu}_j=\frac{1}{n_2}\sum_{i\in S_j^c}\mathcal{L}(Z_{S_j};Z_i)$. For the purpose of building our estimator, proceed as if $\mathcal{L}(Z_{S_j};Z_i)$ depended only on $Z_i$ and $n_1$: the loss does not depend on the actual $n_1$ training examples $Z_{S_j}$, but only on the number of training examples and on the test example. Then the correlation between the $\hat{\mu}_j$'s becomes $n_2/(n_1+n_2)$. Indeed, when $\mathcal{L}(Z_{S_j};Z_i)=f(Z_i)$, we have

$$
\hat {\mu} _ {1} = \frac {1}{n _ {2}} \sum_ {i = 1} ^ {n} I _ {1} (i) f (Z _ {i}) \quad \text { and } \quad \hat {\mu} _ {2} = \frac {1}{n _ {2}} \sum_ {k = 1} ^ {n} I _ {2} (k) f (Z _ {k}),
$$

where $I _ { 1 } ( i )$ is equal to 1 if $Z _ { i }$ is a test example for $\hat { \mu } _ { 1 }$ and is equal to 0 otherwise. Naturally, $I _ { 2 } ( k )$ is defined similarly. We obviously have $\operatorname{Var} [ \hat { \mu } _ { 1 } ] = \operatorname{Var} [ \hat { \mu } _ { 2 } ]$ with 

$$
\begin{array}{l} \operatorname{Var} [ \hat {\mu} _ {1} ] = E [ \operatorname{Var} [ \hat {\mu} _ {1} \mid I _ {1} (\cdot) ] ] + \operatorname{Var} [ E [ \hat {\mu} _ {1} \mid I _ {1} (\cdot) ] ] \\ \qquad = E \left[ \frac {\operatorname{Var} [ f (Z _ {1}) ]}{n _ {2}} \right] + \operatorname{Var} [ E [ f (Z _ {1}) ] ] = \frac {\operatorname{Var} [ f (Z _ {1}) ]}{n _ {2}}, \end{array}
$$

where $I _ { 1 } ( \cdot )$ denotes the $n \times 1$ vector made of the $I _ { 1 } ( i ) ^ { \prime } { \bf s }$ . Moreover, 

$$
\begin{array}{l} \operatorname{Cov} [ \hat {\mu} _ {1}, \hat {\mu} _ {2} ] = E [ \operatorname{Cov} [ \hat {\mu} _ {1}, \hat {\mu} _ {2} \mid I _ {1} (\cdot), I _ {2} (\cdot) ] ] \\ \qquad + \operatorname{Cov} [ E [ \hat {\mu} _ {1} \mid I _ {1} (\cdot), I _ {2} (\cdot) ], E [ \hat {\mu} _ {2} \mid I _ {1} (\cdot), I _ {2} (\cdot) ] ] \\ \qquad = E \left[ \frac {1}{n _ {2} ^ {2}} \sum_ {i = 1} ^ {n} I _ {1} (i) I _ {2} (i) \operatorname{Var} [ f (Z _ {i}) ] \right] + \operatorname{Cov} [ E [ f (Z _ {1}) ], E [ f (Z _ {1}) ] ] \\ \qquad = \frac {\operatorname{Var} [ f (Z _ {1}) ]}{n _ {2} ^ {2}} \sum_ {i = 1} ^ {n} \frac {n _ {2} ^ {2}}{n ^ {2}} + 0 = \frac {\operatorname{Var} [ f (Z _ {1}) ]}{n}, \end{array}
$$

so that the correlation between $\hat { \mu } _ { 1 }$ and $\hat { \mu } _ { 2 } ( \hat { \mu } _ { j }$ and $\hat { \mu } _ { j ^ { \prime } }$ with $j \neq j ^ { \prime }$ in general) is $\textstyle { \frac { n _ { 2 } } { n } }$ Therefore our first estimator of Var[ $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ is $\begin{array} { r } { ( \frac { 1 } { J } + \frac { \rho _ { o } } { 1 - \rho _ { o } } ) S _ { \hat { \mu } } ^ { 2 } } \end{array}$ where $\rho _ { o } = \rho _ { o } ( n _ { 1 } , n _ { 2 } ) =$ $\frac { n _ { 2 } } { n _ { 1 } + n _ { 2 } }$ , that is $\begin{array} { r } { ( \frac { 1 } { J } + \frac { n _ { 2 } } { n _ { 1 } } ) S _ { \hat { \mu } _ { i } } ^ { 2 } } \end{array}$ This will tend to overestimate or underestimate Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ according to whether $\rho _ { o } > \rho$ or $\rho _ { o } < \rho$ 

By construction, $\rho _ { o }$ will be a good substitute for ρ when $\mathcal { L } ( Z _ { S _ { i } } ; Z )$ does not depend much on the training set $Z _ { S _ { j } }$ , that is when the decision function of the underlying algorithm does not change too much when different training sets are chosen. Here are instances where we might suspect this to be true. 

- The capacity (VC dimension) of the algorithm is not too large relative to the size of the training set (for instance a parametric model that is not too complex). 

- The algorithm is robust relative to perturbations in the training set. For instance, one could argue that the support vector machine (Burges, 1998) would tend to fall in this category. Classification and regression trees (Breiman et al., 1984) however will typically not have this property as a slight modification in data may lead to substantially different tree growths so that for two different training sets, the corresponding decision functions (trees) obtained may differ substantially on some regions. K -nearest neighbors techniques will also lead to substantially different decision functions when different training sets are used, especially if K is small. 

## 3.2. Second method: Overestimating $\operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$

Our second method aims at overestimating Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ . As explained in Appendix A, this leads to conservative inference, that is tests of hypothesis with actual size less than the nominal size. This is important because techniques currently in use have the opposite defect, that is they tend to be liberal (tests with actual size exceeding the nominal size), which is normally regarded as less desirable than conservative tests. 

We have shown at the end of Section 2 that ${}_{n_1}^{n_2}\sigma_J^2 = \operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$ could not be estimated unbiasedly without some prior knowledge about $\sigma_0,\sigma_1,\sigma_2,\sigma_3$ (we showed after (10) how this can be done when $\rho=\sigma_2/\sigma_1$ is known). However, as we show below, we may estimate unbiasedly ${}_{n_1'}^{n_2}\sigma_J^2 = \operatorname{Var}[{}_{n_1'}^{n_2}\hat{\mu}_J]$, where $n_1'=\lfloor n/2\rfloor-n_2<n_1$ (we assume $n_2<\lfloor n/2\rfloor$). Let ${}_{n_1'}^{n_2}\hat{\sigma}_J^2$ be the unbiased estimator, developed below, of the above variance. Since $n_1'<n_1$, Conjecture 1 gives $\operatorname{Var}[{}_{n_1'}^{n_2}\hat{\mu}_J] \geq \operatorname{Var}[{}_{n_1}^{n_2}\hat{\mu}_J]$, so that ${}_{n_1'}^{n_2}\hat{\sigma}_J^2$ will tend to overestimate ${}_{n_1}^{n_2}\sigma_J^2$.

Here’s how we may estimate ${}_{n_1'}^{n_2}\sigma_J^2$ without bias. The main idea is that we can get two independent instances of ${ } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ which allows us to estimate $\begin{array} { l } { { n _ { 2 } } } \\ { { n _ { 1 } ^ { \prime } } } \end{array} \sigma _ { J } ^ { 2 }$ without bias. Of course variance estimation from only two observations is noisy. Fortunately, the process by which this variance estimate is obtained can be repeated at will, so that we may have many unbiased estimates of $\begin{array} { l } { { n _ { 2 } } } \\ { { n _ { 1 } ^ { \prime } } } \end{array} \sigma _ { J } ^ { 2 }$ . Averaging these yields a more accurate estimate of $\begin{array} { l } { { n _ { 2 } } } \\ { { n _ { 1 } ^ { \prime } } } \end{array} \sigma _ { J } ^ { 2 }$ 

Obtaining a pair of independent $_ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \hat { \mu } _ { J } \mathrm { ' s }$ is simple. Suppose, as before, that our data set $Z _ { 1 } ^ { n }$ consists of $n = n _ { 1 } + n _ { 2 }$ examples. For simplicity, assume that n is $\mathrm { e v e n . } ^ { 2 }$ We have to randomly split our data $Z _ { 1 } ^ { n }$ into two distinct data sets, $D _ { 1 }$ and $D _ { 1 } ^ { c }$ , of size $\left\lfloor { \frac { n } { 2 } } \right\rfloor$ each. Let $\hat { \mu } _ { ( 1 ) }$ be the statistic of interest $( \mathbf { \Pi } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \hat { \mu } _ { J } )$ computed on $D _ { 1 }$ . This involves, among other things, drawing J train/test subsets from $D _ { 1 } ,$ respectively of size $n _ { 1 } ^ { \prime }$ and $n _ { 2 }$ . Let $\hat { \mu } _ { ( 1 ) } ^ { c }$ be the statistic computed on $D _ { 1 } ^ { c }$ . Then $\hat { \mu } _ { ( 1 ) }$ and $\hat { \mu } _ { ( 1 ) } ^ { c }$ are independent since $D _ { 1 }$ and $D _ { 1 } ^ { c }$ are independent data sets,<sup>3</sup> so that $\begin{array} { r } { ( \hat { \mu } _ { ( 1 ) } - \frac { \hat { \mu } _ { ( 1 ) } + \hat { \mu } _ { ( 1 ) } ^ { c } } { 2 } ) ^ { 2 } + ( \hat { \mu } _ { ( 1 ) } ^ { c } - \frac { \hat { \mu } _ { ( 1 ) } + \hat { \mu } _ { ( 1 ) } ^ { c } } { 2 } ) ^ { 2 } = \frac { 1 } { 2 } ( \hat { \mu } _ { ( 1 ) } - \hat { \mu } _ { ( 1 ) } ^ { c } ) ^ { 2 } } \end{array}$ is unbiased for ${}_{n_1'}^{n_2}\sigma_J^2$ . This splitting process may be repeated $M$ times. This yields $D _ { m }$ and $D _ { m } ^ { c }$ , with $D _ { m } \stackrel { \cdot \cdot _ { 1 } } { \cup } \bar { D } _ { m } ^ { c } = Z _ { 1 } ^ { n } , D _ { m } \cap D _ { m } ^ { c } = \varnothing$ and $| D _ { m } | = | D _ { m } ^ { c } | = \lfloor \frac { n } { 2 } \rfloor$ for $m = 1 , \ldots , M$ 

Each split yields a pair $( \hat { \mu } _ { ( m ) } , \hat { \mu } _ { ( m ) } ^ { c } )$ that is such that 

$$
E \left[ \frac {\left(\hat {\mu} _ {(m)} - \hat {\mu} _ {(m)} ^ {c}\right) ^ {2}}{2} \right] = \frac {1}{2}   \mathrm{Var} \big [ \hat {\mu} _ {(m)} - \hat {\mu} _ {(m)} ^ {c} \big ] = \frac {\mathrm{Var} \big [ \hat {\mu} _ {(m)} \big ] + \mathrm{Var} \big [ \hat {\mu} _ {(m)} ^ {c} \big ]}{2} = \mathop {n _ {2}} _ {n _ {1} ^ {\prime}} \sigma_ {J} ^ {2}.
$$

This allows us to use the following unbiased estimator of ${ } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \sigma _ { J } ^ { 2 }$ : 

$$
{ } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \hat { \sigma } _ { J } ^ { 2 } = \frac { 1 } { 2 M } \sum _ { m = 1 } ^ { M } \left( \hat { \mu } _ { ( m ) } - \hat { \mu } _ { ( m ) } ^ { c } \right) ^ { 2 } .\tag{11}
$$

Note that, according to Lemma 1, the variance of the proposed estimator is $\operatorname{Var}[{}_{n_1'}^{n_2}\hat{\sigma}_J^2] = \frac{1}{4}\operatorname{Var}[(\hat{\mu}_{(m)}-\hat{\mu}_{(m)}^c)^2]\left(r+\frac{1-r}{M}\right)$, with $r=\operatorname{Corr}[(\hat{\mu}_{(m)}-\hat{\mu}_{(m)}^c)^2,(\hat{\mu}_{(m')}-\hat{\mu}_{(m')}^c)^2]$ for $m\ne m'$. We may deduce from Lemma 1 that $r>0$, but simulations yielded $r$ close to 0, so that $\operatorname{Var}[{}_{n_1'}^{n_2}\hat{\sigma}_J^2]$ decreased roughly like $1/M$. We provide some guidance on the choice of $M$ in Section 5.

Note that the computational effort to obtain this variance estimator is proportional to JM. We could reduce this by a factor J if we use $\begin{array} { c } { { n _ { 2 } } } \\ { { n _ { 1 } ^ { \prime } } } \end{array} \hat { \sigma } _ { 1 } ^ { 2 }$ to overestimate Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ]$ , but we suspect that overestimation might be too gross as ${ } ^ { l _ { 1 } } E [ { } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \hat { \sigma } _ { 1 } ^ { 2 } ] = { } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \sigma _ { 1 } ^ { 2 } \ge { } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \sigma _ { J } ^ { 2 } \ge { } _ { n _ { 1 } } ^ { n _ { 2 } } \sigma _ { J } ^ { 2 }$ . We considered this ultra-conservative estimator of $^ { n _ { 2 } } _ { n _ { 1 } } \sigma _ { J } ^ { 2 }$ when we performed the simulations presented in Section 5 but, as we suspected, the resulting inference was too conservative. We do not show the results to avoid overcrowding the paper. We could also have gone half way by using $\begin{array} { l } { { n _ { 2 } } } \\ { { n _ { 1 } ^ { \prime } } } \end{array} \hat { \sigma } _ { J } ^ { 2 }$ <sub></sub> with $1 < J ^ { \prime } < J$ , but we did not pursue this for the same reason as above. 

## 4. Inference about ${}_{n_1}\mu$

We present seven different techniques to perform inference (confidence interval or test) about $n _ { 1 } \mu$ . The first three are methods already in use in the machine-learning community, the others are methods we put forward. Among these new methods, two were shown in the previous section; the other two are the “pseudo-bootstrap” and corrected “pseudo-bootstrap” (described later). Tests<sup>4</sup> of the hypothesis $H _ { 0 } \colon _ { n _ { 1 } } \mu = \mu _ { 0 }$ (at significance level α) have the following form 

$$
\text { reject } H _ {0} \quad \text { if } | \hat {\mu} - \mu_ {0} | > c \sqrt {\hat {\sigma} ^ {2}},\tag{12}
$$

while confidence intervals for $n _ { 1 } \mu$ (at confidence level $1 - \alpha )$ will look like 

$$
_ {n _ {1}} \mu \in [ \hat {\mu} - c \sqrt {\hat {\sigma} ^ {2}}, \hat {\mu} + c \sqrt {\hat {\sigma} ^ {2}} ].\tag{13}
$$

Note that in (12) or (13), µˆ will be an average, $\hat { \sigma } ^ { 2 }$ is meant to be a variance estimate of µˆ and (using the central limit theorem to argue that the distribution of $\hat { \mu }$ is approximately Gaussian) c will be a percentile from the $N ( 0 .$ , 1) distribution or from Student’s t distribution. The only difference between the seven techniques is in the choice of $\hat { \mu } , \hat { \sigma } ^ { 2 }$ and $c .$ In this section we lay out what ${ \hat { \mu } } , { \hat { \sigma } } ^ { 2 }$ and c are for the seven techniques considered and comment on whether each technique should be liberal or conservative based on its political ratio. All this is summarized in Table 1. The properties (size and power of the tests) of those seven techniques shall be investigated in Section 5. 


Table 1. Summary description of the seven inference methods considered in relation to the rejection criteria shown in (12) or the confidence interval shown in (13).


<table><tr><td>Name</td><td><eq>\hat{\mu}</eq></td><td><eq>\hat{\sigma}^{2}</eq></td><td>c</td><td><eq>\frac{\text{Var}[\hat{\mu}]}{E[\hat{\sigma}^{2}]}</eq></td></tr><tr><td>1. t-test (McNemar)</td><td><eq>_{n_{1}}^{n_{2}}\hat{\mu}_{1}</eq></td><td><eq>\frac{1}{n_{2}}S_{L}^{2}</eq></td><td><eq>z_{1-\alpha/2}</eq></td><td><eq>\frac{n_{2}\sigma_{3}+(\sigma_{0}-\sigma_{3})}{\sigma_{0}-\sigma_{3}}&gt;1</eq></td></tr><tr><td>2. Resampled t</td><td><eq>_{n_{1}}^{n_{2}}\hat{\mu}_{J}</eq></td><td><eq>\frac{1}{J}S_{\hat{\mu}_{j}}^{2}</eq></td><td><eq>t_{J-1,1-\alpha/2}</eq></td><td><eq>1+J\frac{\rho}{1-\rho}&gt;1</eq></td></tr><tr><td>3. Dietterich&#x27;s 5 × 2 cv</td><td><eq>_{n/2}^{n/2}\hat{\mu}_{1}</eq></td><td><eq>\hat{\sigma}_{Diet}^{2}</eq></td><td><eq>t_{5,1-\alpha/2}</eq></td><td><eq>\frac{\sigma_{1}}{\sigma_{1}-\sigma_{4}}</eq></td></tr><tr><td>4. Conservative Z</td><td><eq>_{n_{1}}^{n_{2}}\hat{\mu}_{J}</eq></td><td><eq>_{n_{1}^{\prime}}^{n_{2}}\hat{\sigma}_{J}^{2}</eq></td><td><eq>z_{1-\alpha/2}</eq></td><td><eq>\frac{_{n_{1}}^{n_{2}}\sigma_{J}^{2}}{_{n_{1}^{\prime}}\sigma_{J}^{2}}&lt;1</eq></td></tr><tr><td>5. Pseudo-bootstrap</td><td><eq>_{n_{1}}^{n_{2}}\hat{\mu}_{J}</eq></td><td><eq>\check{\sigma}^{2}</eq></td><td><eq>t_{R-1,1-\alpha/2}</eq></td><td><eq>1+J\frac{\rho}{1-\rho}&gt;1</eq></td></tr><tr><td>6. Corrected resampled t</td><td><eq>_{n_{1}}^{n_{2}}\hat{\mu}_{J}</eq></td><td><eq>(\frac{1}{J}+\frac{n_{2}}{n_{1}})S_{\hat{\mu}_{j}}^{2}</eq></td><td><eq>t_{J-1,1-\alpha/2}</eq></td><td><eq>\frac{1+J\frac{\rho}{1-\rho}}{1+J\frac{n_{2}}{n_{1}}}</eq></td></tr><tr><td>7. Corrected pseudo-bootstrap</td><td><eq>_{n_{1}}^{n_{2}}\hat{\mu}_{J}</eq></td><td><eq>(1+\frac{Jn_{2}}{n_{1}})\check{\sigma}^{2}</eq></td><td><eq>t_{R-1,1-\alpha/2}</eq></td><td><eq>\frac{1+J\frac{\rho}{1-\rho}}{1+J\frac{n_{2}}{n_{1}}}</eq></td></tr></table>


$z _ { p }$ and $t _ { k , p }$ refer to the quantile $p$ of the N (0, 1) and Student's $t _ { k }$ distributions respectively. 



The political ratio, that is $\frac { \operatorname{Var} [ \hat { \mu } ] } { E [ \hat { \sigma } ^ { 2 } ] } ,$ , indicates if inference according to the corresponding method will tend to be conservative (ratio less than 1) or liberal (ratio greater than 1). 



See Section 4 for further details. 


We are now ready to introduce the statistics we will consider in this paper. 

1. t -test statistic. Let the available data $Z _ { 1 } ^ { n }$ be split into a training set $Z _ { S _ { 1 } }$ of size $n _ { 1 }$ and a test set $Z _ { S _ { 1 } ^ { c } }$ of size $n _ { 2 } = n - n _ { 1 }$ , with $n_2$ relatively large (a third or a quarter of n for instance). One may consider $\hat { \mu } = { \bf \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { 1 }$ to estimate $n _ { 1 } \mu$ and $\begin{array} { r } { \hat { \sigma } ^ { 2 } = \frac { S _ { L } ^ { 2 } } { n_2 } } \end{array}$ where $S _ { L } ^ { 2 }$ is the sample variance of the $L ( 1 , i ) \mathrm { { ' s } }$ involved in $\begin{array} { r } { { \bf \Xi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { 1 } = n _ { 2 } ^ { - 1 } \sum _ { i \in S _ { 1 } ^ { c } } L ( 1 , i ) . } \end{array}$ Inference would be based on the (incorrect) belief that 

$$
\frac {\frac {n _ {2}}{n _ {1}} \hat {\mu} _ {1} - n _ {1} \mu}{\sqrt {\frac {S _ {L} ^ {2}}{n _ {2}}}} \sim N (0, 1).\tag{14}
$$

We use $N ( 0 , 1 )$ here (instead of $t _ { n _ { 2 } - 1 }$ for instance) as $n _ { 2 }$ is meant to be fairly large (greater than 50, say). 

Lemma 1 tells us that the political ratio here is 

$$
\frac {\operatorname{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {1} \right]}{E \left[ \begin{array}{c} \frac {S _ {L} ^ {2}}{n _ {2}} \end{array} \right]} = \frac {n _ {2} \sigma_ {3} + (\sigma_ {0} - \sigma_ {3})}{\sigma_ {0} - \sigma_ {3}} > 1,
$$

so this approach leads to liberal inference. This phenomenon grows worse as $n _ { 2 }$ increases. Note that $S _ { L } ^ { 2 }$ is a biased estimator of $\sigma _ { 0 }$ (the unconditional variance of $L ( 1 , i ) ~ =$ 

$L ( Z _ { S _ { 1 } } ; Z _ { i } ) , ~ i ~ \notin ~ S _ { 1 } )$ , but is unbiased for the variance of $L ( 1 , i )$ conditional on the training set $Z _ { S _ { 1 } } . ^ { 6 }$ That is so because, given $Z _ { S _ { 1 } }$ , the $L ( 1 , i ) \mathbf { \dot { s } }$ are independent variates. Therefore, although (14) is wrong, we do have 

$$
\frac {\frac {n _ {2}}{n _ {1}} \hat {\mu} _ {1} - E \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {1} \mid Z _ {S _ {1}} \right]}{\sqrt {\frac {S _ {L} ^ {2}}{n _ {2}}}} \approx N (0, 1)
$$

in so far as $n _ { 2 }$ is large enough for the central limit theorem to apply. Therefore this method really allows us to make inference about $E [ { } ~ { } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { 1 } ~ | ~ Z _ { S _ { 1 } } ] = E [ L ( 1 , i ) ~ | ~ Z _ { S _ { 1 } } ] =$ $E [ \mathcal { L } ( Z _ { S _ { 1 } } ; Z _ { i } ) ~ | ~ Z _ { S _ { 1 } } ] , ~ i ~ \notin ~ S _ { 1 }$ , that is the generalization error of the specific rule obtained by training the algorithm on $Z _ { S _ { 1 } }$ , not the generalization error of the algorithm per se. That is, according to Dietterich’s taxonomy (Dietterich, 1998) briefly explained in Section 1, it deals with questions of type 1 through 4 rather than questions of type 5 through 8. 

2. Resampled t-test statistic. Let us refresh some notation from Section 1. In particular, recall that ${}_{n_1}^{n_2}\hat{\mu}_J=J^{-1}\sum_{j=1}^{J}\hat{\mu}_j$. The resampled t-test technique⁷ considers $\hat{\mu}={}_{n_1}^{n_2}\hat{\mu}_J$ and $\hat{\sigma}^2=S_{\hat{\mu}_j}^2/J$, where $S_{\hat{\mu}_j}^2$ is the sample variance of the $\hat{\mu}_j$'s (see (9)). Inference would be based on the (incorrect) belief that

$$
\frac {\frac {n _ {2}}{n _ {1}} \hat {\mu} _ {J} - n _ {1} \mu}{\sqrt {\frac {S _ {\hat {\mu} _ {j}} ^ {2}}{J}}} \sim t _ {J - 1}.\tag{15}
$$

Combining (8) and Lemma 1 gives us the following political ratio 

$$
\frac {\operatorname{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right]}{E \left[ \frac {S _ {\hat {\mu} _ {j}} ^ {2}}{J} \right]} = \frac {J \operatorname{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right]}{E \left[ S _ {\hat {\mu} _ {j}} ^ {2} \right]} = \frac {J \sigma_ {2} + (\sigma_ {1} - \sigma_ {2})}{\sigma_ {1} - \sigma_ {2}} > 1,
$$

so this approach leads to liberal inference, a phenomenon that grows worse as J increases. Dietterich (1998) observed this empirically through simulations. 

As argued in Section $2 , S_{\hat{\mu}_j} ^ { 2 } / J$ actually estimates (without bias) the variance of $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ conditional on $Z _ { 1 } ^ { n }$ . Thus while (15) is wrong, we do have 

$$
\frac {{} _ {n _ {1}} ^ {n _ {2}} \hat {\mu} _ {J} - E \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \mid Z _ {1} ^ {n} \right]}{\sqrt {\frac {S_{\hat{\mu}_j} ^ {2}}{J}}} \approx t _ {J - 1}.
$$

Recall from the discussion following (8) that $\begin{array} { r l } { E [ { \mathbf \Lambda } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } | Z _ { 1 } ^ { n } ] = } & { { } { \mathbf \Lambda } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty } } \end{array}$ . Therefore this method really allows us to make inference about $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty }$ , which is not too useful because we want to make inference about $_ { n _ { 1 } \mu }$ 

3. $5 \times 2$ cv t -test. Dietterich $( 1 9 9 8 ) ^ { 8 }$ split $Z _ { 1 } ^ { n }$ in half $M = 5$ times to yield $D _ { 1 } , D _ { 1 } ^ { c } , \ldots ,$ $D _ { 5 } , D _ { 5 } ^ { c }$ as in Section 3 and let 

$$
\tilde {\mu} _ {(m)} = \lfloor n / 2 \rfloor^ {- 1} \sum_ {i \in D _ {m} ^ {c}} \mathcal {L} (D _ {m}; Z _ {i}), \quad \tilde {\mu} _ {(m)} ^ {c} = \lfloor n / 2 \rfloor^ {- 1} \sum_ {i \in D _ {m}} \mathcal {L} (D _ {m} ^ {c}; Z _ {i}).
$$

He then used $\begin{array} { r } { \hat { \mu } = \tilde { \mu } _ { ( 1 ) } , \hat { \sigma } ^ { 2 } = \hat { \sigma } _ { D i e t } ^ { 2 } = \frac { 1 } { 1 0 } \sum _ { m = 1 } ^ { 5 } ( \tilde { \mu } _ { ( m ) } - \tilde { \mu } _ { ( m ) } ^ { c } ) ^ { 2 } } \end{array}$ and $c = t _ { 5 , 1 - \alpha / 2 }$ . Note that the political ratio is 

$$
\frac {\mathrm{Var} \big [ \tilde {\mu} _ {(1)} \big ]}{E [ \hat {\sigma} ^ {2} ]} = \frac {\sigma_ {1} (\lfloor n / 2 \rfloor , \lfloor n / 2 \rfloor)}{\sigma_ {1} (\lfloor n / 2 \rfloor , \lfloor n / 2 \rfloor) - \sigma_ {4}}
$$

where $\sigma _ { 4 } = \operatorname{Cov} [ \tilde { \mu } _ { ( m ) } , \tilde { \mu } _ { ( m ) } ^ { c } ]$ 

Remarks 

- As Dietterich noted, this allows inference for $\lfloor n / 2 \rfloor \mu$ which may be substantially distant from ${ } _ { n } \mu$ 

- The choice of $M = 5$ seems arbitrary. 

- The statistic was developed under the assumption that the $\tilde { \mu } _ { ( m ) } 's$ and $\tilde { \mu } _ { ( m ) } ^ { c } \mathrm { : }$ are 10 independent and identically distributed Gaussian variates. Even in this ideal case, 

$$
t _ {D} = \frac {\hat {\mu} - \lfloor n / 2 \rfloor \mu}{\sqrt {\hat {\sigma} ^ {2}}} = \frac {\tilde {\mu} _ {(1)} - \lfloor n / 2 \rfloor \mu}{\sqrt {\frac {1}{1 0} \sum_ {m = 1} ^ {5} \left(\tilde {\mu} _ {(m)} - \tilde {\mu} _ {(m)} ^ {c}\right) ^ {2}}}\tag{16}
$$

is not distributed as $t _ { 5 }$ as assumed in Dietterich (1998) because $\tilde { \mu } _ { ( 1 ) }$ and $( \tilde { \mu } _ { ( 1 ) } - \tilde { \mu } _ { ( 1 ) } ^ { c } )$ are not independent. That is easily fixed in two different ways: 

– Take the sum from $m = 2$ to $m = 5$ and replace 10 by 8 in the denominator of (16) which would result in $t _ { D } \sim t _ { 4 } .$ 

– Replace the numerator by $\sqrt { 2 } ( { \textstyle \frac { \tilde { \mu } _ { ( 1 ) } + \tilde { \mu } _ { ( 1 ) } ^ { c } } { 2 } } - { } _ { \lfloor n / 2 \rfloor } \mu )$ which would lead to $t _ { D } \sim t _ { 5 }$ as $\tilde { \mu } _ { ( 1 ) } + \tilde { \mu } _ { ( 1 ) } ^ { c }$ and $\tilde { \mu } _ { ( 1 ) } - \tilde { \mu } _ { ( 1 ) } ^ { c }$ are independent. 

In all cases, more degrees of freedom could be exploited; statistics distributed as $t _ { 8 }$ can be devised by appropriate use of the 10 (assumed) independent variates. 

4. Conservative Z. We estimate $n _ { 1 } \mu$ by $\hat { \mu } = { \bf \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ and use $\hat { \sigma } ^ { 2 } = \begin{array} { l } { n _ { 2 } } \\ { n _ { 1 } ^ { \prime } } \end{array} \hat { \sigma } _ { J } ^ { 2 }$ (Eq. (11)) as its conservative variance estimate. Since ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ is the mean of many $( J n _ { 2 }$ to be exact) $L(j,i)$'s , we may expect that its distribution is approximatively normal. We then proceed as if 

$$
Z = \frac {{\bf \Pi} _ {n _ {1}} ^ {n _ {2}} \hat {\mu} _ {J} - {\bf \Pi} _ {n _ {1}} \mu}{\sqrt {{\bf \Pi} _ {n _ {1} ^ {\prime}} ^ {n _ {2}} \hat {\sigma} _ {J} ^ {2}}}\tag{17}
$$

was a $N ( 0 , 1 )$ variate (even though $\begin{array} { l } { { n _ { 2 } } } \\ { { n _ { 1 } ^ { \prime } } } \end{array} \hat { \sigma } _ { J } ^ { 2 }$ is designed to overestimate Var[ ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ] )$ to perform inference, leading us to use $\begin{array} { r } { \begin{array} { r c l } { \dot { \mathbf { \boldsymbol { { c } } } } } & { = } & { \boldsymbol { { z } } _ { 1 - \alpha / 2 } } \end{array} } \end{array}$ in (12) or (13), where $z _ { 1 - \alpha / 2 }$ is the percentile $1 - \alpha$ of the $N ( 0 , 1 )$ distribution. Some would perhaps prefer to use percentile from the t distribution, but it is unclear what the degrees of freedom ought to be. People like to use the t distribution in approximate inference frameworks, such as the one we are dealing with, to yield conservative inference. This is unnecessary here as inference is already conservative via the variance overestimation. Indeed, the political ratio 

$$
\frac {\mathrm{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right]}{E \left[ \begin{array}{c} n _ {2} \\ n _ {1} ^ {\prime} \end{array} \hat {\sigma} _ {J} ^ {2} \right]} = \frac {\stackrel {{n _ {2}}} {{n _ {1}}} \sigma_ {J} ^ {2}}{\stackrel {{n _ {2}}} {{n _ {1} ^ {\prime}}} \sigma_ {J} ^ {2}}
$$

is smaller than 1 if we believe in Conjecture 1. 

Regarding the choice of $n _ { 2 }$ (and thus $n _ { 1 } )$ , we may take it to be small relatively to n (the total number of examples available). One may use $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ for instance provided J is not smallish. 

5. Pseudo-Bootstrap. To estimate the variance of $\begin{array} { r } { \hat { \mu } = \begin{array} { r } { n _ { 2 } } \\ { n _ { 1 } } \end{array} \hat { \mu } _ { J } } \end{array}$ by a procedure similar to the bootstrap (Efron & Tibshirani, 1993), we obtain R other instances of that random variable, by redoing the computation with different splits on the same data $Z _ { 1 } ^ { n }$ ; call these $\check { \mu } _ { 1 } , \dots , \check { \mu } _ { R }$ . Thus, in total, $( R + 1 ) J$ training and testing sets are needed here. Then one could consider $\hat { \sigma } ^ { 2 } = \check { \sigma } ^ { 2 }$ , where $\check { \sigma } ^ { 2 }$ is the sample variance of $\check { \mu } _ { 1 } , \dots , \check { \mu } _ { R }$ , and take $c = t _ { R - 1 , 1 - \alpha / 2 }$ , as $\check { \sigma } ^ { 2 }$ has $R - 1$ degrees of freedom. Of course ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } , \check { \mu } _ { 1 } , \dots , \check { \mu } _ { R }$ are $R + 1$ identically distributed random variables. But they are not independent as we find, from (7), that the covariance between them is $\sigma _ { 2 }$ . Using Lemma 1, we have 

$$
\frac {\mathrm{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right]}{E [ \check {\sigma} ^ {2} ]} = \frac {\stackrel {{n _ {2}}} {{n _ {1}}} \sigma_ {J} ^ {2}}{\stackrel {{n _ {2}}} {{n _ {1}}} \sigma_ {J} ^ {2} - \sigma_ {2}} = \frac {J \sigma_ {2} + (\sigma_ {1} - \sigma_ {2})}{\sigma_ {1} - \sigma_ {2}} > 1.
$$

Note that this political ratio is the same as its counterpart for the resampled t-test because $E [ \check { \sigma } ^ { 2 } ] = E [ \frac { S _ { \hat { \mu } _ { j } } ^ { 2 } } { J } ]$ . So the pseudo-bootstrap leads to liberal inference that should worsen with increasing J just like the resampled t-test statistic. In other words, the pseudo-bootstrap only provides a second estimator of $\frac { \sigma _ { 1 } - \sigma _ { 2 } } { J }$ which is more complicated and harder to compute than $\frac { S _ { \hat { \mu } _ { j } } ^ { 2 } } { J }$ which is also unbiased for $\frac { \sigma _ { 1 } - \sigma _ { 2 } } { J }$ 

6. Corrected resampled t-test statistic. From our discussion in Section $^ { 3 , }$ we know that an unbiased estimator of $^ { n _ { 2 } } _ { n _ { 1 } } \sigma _ { J } ^ { 2 }$ is $\begin{array} { r } { ( \frac { 1 } { J } + \frac { \rho } { 1 - \rho } ) S _ { \hat { \mu } _ { j } } ^ { 2 } } \end{array}$ , where $S _ { \hat { \mu } } ^ { 2 }$ is the sample variance of the $\hat { \mu } _ { j } { } ^ { \ ' } \mathbf { s }$ . Unfortunately $\rho ,$ , the correlation between the $\hat { \mu } _ { j } \mathrm { ' s }$ , is unknown. The resampled t-test boldly puts $\rho = 0$ . We propose here to proceed as if $\begin{array} { r } { \rho = \rho _ { 0 } = \frac { n _ { 2 } } { n _ { 1 } + n _ { 2 } } } \end{array}$ as our argument in Section 3 suggests. So we use $\begin{array} { r } { \hat { \sigma } ^ { 2 } = ( \frac { 1 } { J } + \frac { n _ { 2 } } { n _ { 1 } } ) S _ { \hat { \mu } _ { i } } ^ { 2 } } \end{array}$ . We must say again that this approximation is gross, but we feel it is better than putting $\rho = 0$ . Furthermore, in the ideal case where the vector of the $\hat { \mu } _ { j } \mathrm { ' s }$ follows the multivariate Gaussian distribution and $\rho$ is actually equal to $\rho _ { 0 }$ , Lemma 2 states that $\frac { \mathbf { \Phi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } - \mathbf { \Phi } _ { n _ { 1 } } \mu } { \sqrt { \hat { \sigma } ^ { 2 } } } \sim t _ { J - 1 }$ . This is why we use $c = t _ { J - 1 , 1 - \alpha / 2 }$ 

Finally, let us note that the political ratio 

$$
\frac {\mathrm{Var} \left[ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {J} \right]}{E [ \hat {\sigma} ^ {2} ]} = \frac {\frac {1}{J} + \frac {\rho}{1 - \rho}}{\frac {1}{J} + \frac {n _ {2}}{n _ {1}}}
$$

will be greater than 1 (liberal inference) if $\rho > \rho _ { 0 } . \mathrm { I f } \rho < \rho _ { 0 }$ , the above ratio is smaller than 1, so that we must expect the inference to be conservative. Having mentioned earlier that conservative inference is preferable to liberal inference, we therefore hope that the ad hoc $\begin{array} { r } { \rho _ { 0 } = \frac { n _ { 2 } } { n _ { 1 } + n _ { 2 } } } \end{array}$ will tend to be larger than the actual correlation $\rho$ . 

7. Corrected pseudo-bootstrap statistic. Naturally, the correction we made in the resampled t-test can be applied to the pseudo-bootstrap procedure as well. Namely, we note that $\begin{array} { r } { ( 1 + J \frac { \rho } { 1 - \rho } ) \check { \sigma } ^ { 2 } } \end{array}$ , where $\check { \sigma } ^ { 2 }$ is the sample variance of the $\check { \mu } _ { r } \mathrm { \bf ~ s } .$ , is unbiased for $^ { n _ { 2 } } _ { n _ { 1 } } \sigma _ { J } ^ { 2 }$ . Naively replacing $\rho$ by $\rho _ { 0 }$ leads us to use $\begin{array} { r } { \hat { \sigma } ^ { 2 } = ( 1 + \frac { J n _ { 2 } } { n _ { 1 } } ) \check { \sigma } ^ { 2 } } \end{array}$ . Furthermore, in the ideal case where $\rho$ is actually equal to $\rho _ { 0 } .$ , and the vector made of $ \mathbf { \Sigma } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } , \check { \mu } _ { 1 } , \dots \check { \mu } _ { R }$ follows the multivariate Gaussian distribution, Lemma 2 states that $\frac { n _ { 2 } \hat { \mu } _ { J } - { \bf \mu } _ { n _ { 1 } } \mu } { \sqrt { \hat { \sigma } ^ { 2 } } } \sim t _ { R - 1 }$ . This is why we use $c = t _ { R - 1 , 1 - \alpha / 2 }$ . Finally note that, just like in the corrected resampled t -test, the political ratio is 

$$
\frac {\mathrm{Var} \big [   _ {n _ {1}} ^ {n _ {2}} \hat {\mu} _ {J} \big ]}{E [ \hat {\sigma} ^ {2} ]} = \frac {\frac {1}{J} + \frac {\rho}{1 - \rho}}{\frac {1}{J} + \frac {n _ {2}}{n _ {1}}}.
$$

We conclude this section by providing in Table 1 a summary of the seven inference methods considered in the present section. 

## 5. Simulation study

We performed a simulation study to investigate the power and the size of the seven statistics considered in the previous section. We also want to make recommendations on the value of J to use for those methods that involve ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ . Simulation results will also lead to a recommendation on the choice of M when the conservative $Z$ is used. 

We will soon introduce the three kinds of problems we considered to cover a good range of possible applications. For a given problem, we shall generate 1000 independent sets of data of the form $\{ Z _ { 1 } , \ldots , Z _ { n } \}$ . Once a data set $Z _ { 1 } ^ { n } = \{ Z _ { 1 } , \ldots Z _ { n } \}$ has been generated, we may compute confidence intervals and/or a tests of hypothesis based on the statistics laid out in Section 4 and summarized in Table 1. A difficulty arises however. For a given $n ,$ those seven methods don’t aim at inference for the same generalization error. For instance, Dietterich’s method aims at $n / 2 \mu$ (we take n even for simplicity), while the others aim at $n _ { 1 } \mu$ where $n _ { 1 }$ would usually be different for different methods $\begin{array} { r } { ( { \tt e . g . , } n _ { 1 } = \frac { 2 n } { 3 } } \end{array}$ for the t -test and $\begin{array} { r } { n _ { 1 } = \frac { 9 n } { 1 0 } } \end{array}$ for methods using ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } )$ . In order to compare the different techniques, for a given n, we shall always aim at $n / 2 \mu$ . The use of the statistics other than Dietterich’s $5 \times 2$ cv shall be modified as follows. 

- t-test statistic. We take $\begin{array} { r } { n _ { 1 } = n _ { 2 } = \frac { n } { 2 } } \end{array}$ . This deviates slightly from the normal usage of the t-test where $n _ { 2 }$ is one third, say, of $n ,$ not one half. 

- Methods other that the t-test and Dietterich’s $5 \times 2 ~ c \nu$ . For methods involving $_ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ where J is a free parameter, that is all methods except the t-test and Dietterich’s $5 \times 2 \mathrm { c v } .$ we take $\begin{array} { r } { n _ { 1 } = n _ { 2 } = \frac { n } { \gamma } } \end{array}$ . This deviates substantially from the normal usage where $n _ { 1 }$ would be 5 to 10 times larger than $n _ { 2 }$ , say. For that reason, we also take $\begin{array} { r } { n _ { 1 } = \frac { n } { 2 } } \end{array}$ and $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ (assume n is a multiple of 10 for simplicity). This is achieved by throwing away 40% of the data. Note that when we will address the question of the choice of $J$ (and M for the conservative $Z )$ , we shall use $\begin{array} { r } { n _ { 1 } = \frac { 9 n } { 1 0 } } \end{array}$ and $\textstyle n _ { 2 } = { \frac { n } { 1 0 } }$ , more in line with the normal usage. 

- Conservative Z. For the conservative $Z ,$ we need to explain how we compute the variance estimate. Indeed, formula (11) suggests that we have to compute $^ n _ { 0 } ^ { n _ { 2 } } \hat { \sigma } _ { J } ^ { 2 }$ whenever $n _ { 1 } =$ $\begin{array} { r } { n _ { 2 } = \frac { n } { 2 } ! } \end{array}$ What we do is that we choose $n _ { 2 }$ as we would normally do (10% of n here) and do the variance calculation as usual $\bar { ( } _ { n / 2 - n _ { 2 } } \hat { \sigma } _ { J } ^ { 2 } = { } _ { 2 n / 5 } ^ { n / 1 0 } \hat { \sigma } _ { J } ^ { 2 } )$ . However, as explained above, we use $\mathbf { \Sigma } _ { n / 2 } ^ { n / 2 } \hat { \mu } _ { J }$ and $\mathbf { \Phi } _ { n / 2 } ^ { n _ { 2 } } \hat { \mu } _ { J } = \mathbf { \Phi } _ { n / 2 } ^ { n / 1 0 } \hat { \mu } _ { J } ^ { \prime }$ instead of $\begin{array} { c } { { n _ { 2 } } } \\ { { n - n _ { 2 } } } \end{array}$ as the cross-validation estimators. Recall that we have argued in Section 2 that $^ { n _ { 2 } } _ { n _ { 1 } } \sigma _ { J } ^ { 2 }$ was decreasing in $n _ { 1 }$ and $n _ { 2 }$ . Consequently the variances of $\begin{array} { r } { { n } / { 2 } } \\ { { n } / { 2 } } \end{array}$ and ${ } _ { n / 2 } ^ { n _ { 2 } } \hat { \mu } _ { J }$ are smaller than ${ } _ { n / 2 - n _ { 2 } } \sigma _ { J } ^ { 2 }$ , so that ${ } _ { n / 2 - n _ { 2 } } \hat { \sigma } _ { J } ^ { 2 }$ still acts as a conservative variance estimate, that is 

$$
E \big [ \begin{array}{c} n _ {2} \\ n / 2 - n _ {2} \end{array} \hat {\sigma} _ {J} ^ {2} \big ] = \begin{array}{c} n _ {2} \\ n / 2 - n _ {2} \end{array} \sigma_ {J} ^ {2} = \operatorname{Var} \big [ \begin{array}{c} n _ {2} \\ n / 2 - n _ {2} \end{array} \hat {\mu} _ {J} \big ] \geq \operatorname{Var} \big [ \begin{array}{c} n _ {2} \\ n / 2 \end{array} \hat {\mu} _ {J} \big ] \geq \operatorname{Var} \big [ \begin{array}{c} n / 2 \\ n / 2 \end{array} \hat {\mu} _ {J} \big ].
$$

Thus the variance overestimation will be more severe in the case of $\mathbf { \Pi } _ { n / 2 } ^ { n / 2 } \hat { \mu } _ { J }$ 

We consider three kinds of problems to cover a good range of possible applications: 

1. Prediction in simple normal linear regression. We consider the problem of estimating the generalization error in a simple Gaussian regression problem. We thus have $Z = ( X , Y )$ with $X \sim N ( \mu _ { X } , \sigma _ { X } ^ { 2 } )$ and $Y \mid X \sim N ( a + b X , \sigma _ { Y \mid X } ^ { 2 } )$ where $\sigma _ { Y \mid X } ^ { 2 }$ is constant (does not depend on X). The learning algorithms are 

(A) Sample mean. The decision function is $\begin{array} { r } { F _ { A } ( Z _ { S } ) ( X ) = \frac { 1 } { n _ { 1 } } \sum _ { i \in S } Y _ { i } = \bar { Y } _ { S } } \end{array}$ , that is the mean of the $Y ^ { \ast } { \mathrm { s } }$ in the training set $Z _ { S }$ . Note that this decision function does not depend on X. We use a quadratic loss, so that $L _ { A } ( j , i ) = ( F _ { A } ( Z _ { S _ { i } } ) ( X _ { i } ) - Y _ { i } ) ^ { 2 } =$ $( \bar { Y } _ { S _ { i } } - Y _ { i } ) ^ { 2 }$ 

(B) Linear regression. The decision function is $F _ { B } ( Z _ { S } ) ( X ) = \hat { a } _ { S } + \hat { b } _ { S } X$ where $\hat { a } _ { S }$ and $\hat { b } _ { S }$ are the intercept and the slope of the ordinary least squares regression of Y on X performed on the training set $Z _ { S }$ . Since we use a quadratic loss, we therefore have $L _ { B } ( j , i ) = ( F _ { B } ( Z _ { S _ { j } } ) ( X _ { i } ) - Y _ { i } ) ^ { 2 } = ( \hat { a } _ { S _ { j } } + \hat { b } _ { S _ { j } } X _ { i } - Y _ { i } ) ^ { 2 } .$ 

On top of inference about the generalization errors of algorithm $A ( \underset { n _ { 1 } } { } \mu _ { A } )$ and algorithm $B ( \mathbf { \Phi } _ { n _ { 1 } } \mu _ { B } )$ , we also consider inference about $\ l _ { n _ { 1 } } \mu _ { A - B } = \ l _ { n _ { 1 } } \mu _ { A } - \ l _ { n _ { 1 } } \mu _ { B }$ , the difference of those generalization errors. This inference is achieved by considering $L _ { A - B } ( j , i ) =$ $L _ { A } ( j , i ) - L _ { B } ( j , i )$ 

Table 2 describes the four simulations we performed for the regression problem. For instance, in Simulation 1, we generated 1000 samples of size 200, with $\mu _ { x } = 1 0 $ $\sigma _ { X } ^ { 2 } = 1 , a = 1 0 0 , b = 1$ and $\sigma _ { Y \mid X } ^ { 2 ^ { - } } = 9 7 $ . It is shown in Nadeau and Bengio (1999) that $\textstyle { \phantom { = } } _ { n _ { 1 } } \mu _ { A } = { \frac { n _ { 1 } + 1 } { n _ { 1 } } } ( \sigma _ { Y | X } ^ { 2 } + b ^ { 2 } \sigma _ { X } ^ { 2 } )$ and $\begin{array} { r } { { } _ { n _ { 1 } } \mu _ { B } = \frac { n _ { 1 } + 1 } { n _ { 1 } } \frac { n _ { 1 } - 2 } { n _ { 1 } - 3 } \sigma _ { Y | X } ^ { 2 } } \end{array}$ . Thus the first and third simulation correspond to cases where the two algorithms generalize equally well (for $\begin{array} { r } { n _ { 1 } = \frac { n } { 2 } ) ; } \end{array}$ in the second and fourth case, the linear regression generalizes better than the sample mean.<sup>9</sup> The table also provides some summary confidence intervals for quantities of interest, namely $\begin{array} { r } { { \bf \Phi } _ { n _ { 1 } } \mu , \rho ( n _ { 1 } , n _ { 2 } ) = \frac { \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } ) } { \sigma _ { 1 } ( n _ { 1 } , n _ { 2 } ) } } \end{array}$ and $r$ . 

2. Classification of two Gaussian populations. We consider the problem of estimating the generalization error in a classification problem with two classes. We thus have $Z =$ $( X , Y )$ with Prob $Y = 1 ) = \operatorname{Prob} ( Y = 0 ) = \frac{1}{2} , X \mid Y = 0 \sim N ( \mu _ { 0 } , \Sigma _ { 0 } )$ and $X \mid Y =$ $1 \sim N ( \mu _ { 1 } , \Sigma _ { 1 } )$ . The learning algorithms are 


Table 2. Description of four simulations for the simple linear regression problem.


<table><tr><td></td><td>Simulation 1</td><td>Simulation 2</td><td>Simulation 3</td><td>Simulation 4</td></tr><tr><td>n</td><td>200</td><td>200</td><td>2000</td><td>2000</td></tr><tr><td><eq>\mu_X</eq></td><td>10</td><td>10</td><td>10</td><td>10</td></tr><tr><td>a</td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td>b</td><td>1</td><td>2</td><td>0.1</td><td>0.1</td></tr><tr><td><eq>\sigma_X^2</eq></td><td>1</td><td>2</td><td>1</td><td>5</td></tr><tr><td><eq>\sigma_{Y|X}^2</eq></td><td>97</td><td>64</td><td>9.97</td><td>9</td></tr><tr><td><eq>_{n/2}\mu_A*</eq></td><td>[98.77,100.03]</td><td>[72.30,73.25]</td><td>[9.961,10.002]</td><td>[9.040,9.075]</td></tr><tr><td><eq>_{n/2}\mu_B</eq></td><td>[98.69,99.96]</td><td>[64.89,65.73]</td><td>[9.961,10.002]</td><td>[8.999,9.034]</td></tr><tr><td><eq>_{n/2}\mu_{A-B}*</eq></td><td>[-0.03,0.19]</td><td>[7.25,7.68]</td><td>[-0.001,0.001]</td><td>[0.039,0.043]</td></tr><tr><td><eq>_{9n/10}\mu_A*</eq></td><td>[98.19, 99.64]</td><td>[71.92, 72.99]</td><td>[9.952,9.998]</td><td>[9.026,9.067]</td></tr><tr><td><eq>_{9n/10}\mu_B</eq></td><td>[97.71, 99.16]</td><td>[64.30,65.24]</td><td>[9.948,9.993]</td><td>[8.982,9.023]</td></tr><tr><td><eq>_{9n/10}\mu_{A-B}*</eq></td><td>[0.36,0.60]</td><td>[7.45,7.93]</td><td>[0.003,0.006]</td><td>[0.042,0.047]</td></tr><tr><td><eq>\rho_A(\frac{n}{2},\frac{n}{2})</eq></td><td>[0.466,0.512]</td><td>[0.487,0.531]</td><td>[0.484,0.531]</td><td>[0.471,0.515]</td></tr><tr><td><eq>\rho_B(\frac{n}{2},\frac{n}{2})</eq></td><td>[0.467,0.514]</td><td>[0.473,0.517]</td><td>[0.483,0.530]</td><td>[0.472,0.517]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2},\frac{n}{2})</eq></td><td>[0.225,0.298]</td><td>[0.426,0.482]</td><td>[0.226,0.282]</td><td>[0.399,0.455]</td></tr><tr><td><eq>\rho_A(\frac{n}{2},\frac{n}{10})</eq></td><td>[0.148,0.179]</td><td>[0.165,0.193]</td><td>[0.162,0.194]</td><td>[0.147,0.176]</td></tr><tr><td><eq>\rho_B(\frac{n}{2},\frac{n}{10})</eq></td><td>[0.152,0.183]</td><td>[0.156,0.183]</td><td>[0.162,0.194]</td><td>[0.147,0.175]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2},\frac{n}{10})</eq></td><td>[0.103,0.143]</td><td>[0.146,0.184]</td><td>[0.089,0.128]</td><td>[0.131,0.165]</td></tr><tr><td><eq>\rho_A(\frac{9n}{10},\frac{n}{10})</eq></td><td>[0.090,0.115]</td><td>[0.094,0.117]</td><td>[0.090,0.111]</td><td>[0.088,0.108]</td></tr><tr><td><eq>\rho_B(\frac{9n}{10},\frac{n}{10})</eq></td><td>[0.092,0.117]</td><td>[0.089,0.111]</td><td>[0.090,0.111]</td><td>[0.088,0.108]</td></tr><tr><td><eq>\rho_{A-B}(\frac{9n}{10},\frac{n}{10})</eq></td><td>[0.062,0.091]</td><td>[0.084,0.109]</td><td>[0.059,0.085]</td><td>[0.086,0.109]</td></tr><tr><td><eq>r_A</eq></td><td>[0.021,0.034]</td><td>[0.027,0.040]</td><td>[-0.003,0.008]</td><td>[-0.001,0.008]</td></tr><tr><td><eq>r_B</eq></td><td>[0.022,0.034]</td><td>[0.028,0.043]</td><td>[-0.003,0.008]</td><td>[-0.001,0.009]</td></tr><tr><td><eq>r_{A-B}</eq></td><td>[0.154,0.203]</td><td>[0.071,0.095]</td><td>[0.163,0.202]</td><td>[0.087,0.114]</td></tr></table>


In each of the four simulations, 1000 independent samples of size n where generated with $\mu _ { X } , \ a ,$ $b , \ \sigma _ { X } ^ { 2 }$ and $\sigma _ { Y \mid X } ^ { 2 }$ as shown in the table. 95% confidence intervals for $\begin{array} { r } { { \bf \Pi } _ { n 1 } \mu , \rho ( n _ { 1 } , n _ { 2 } ) = \frac { \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } ) } { \sigma _ { 1 } ( n _ { 1 } ) } } \end{array}$ and $r = \ddot { \operatorname{Corr} } [ ( \hat { \mu } _ { ( m ) } - \hat { \mu } _ { ( m ) } ^ { c } ) ^ { 2 } , ( \hat { \mu } _ { ( m ^ { \prime } ) } - \hat { \mu } _ { ( m ^ { \prime } ) } ^ { c } ) ^ { 2 } ]$ defined after (11) are provided. The subscripts $A \bullet B$ and $A - B$ indicates whether we are working with $L _ { A } , L _ { B }$ or $L _ { A - B } .$ An asterisk besides $\mu$ indicates that powers of tests for tha ${ } , \mu$ are displayed in a figure. 


(A) Regression tree. We train a least square regression $\text{tree} ^ { 1 0 }$ (Breiman et al., 1984) of Y against X and the decision function is $F _ { A } ( Z _ { S } ) ( X ) = I [ N _ { Z _ { S } } ( X ) > 0 . 5 ]$ where $N _ { Z s } ( X )$ is the leaf value corresponding to X of the tree obtained when training on $Z _ { S }$ . Thus $L _ { A } ( j , i ) = I [ F _ { A } ( Z _ { S _ { i } } ) ( { \cal X } _ { i } ) \not = Y _ { i } ]$ is equal to 1 whenever this algorithm misclassifies example i when the training set is $Z _ { S _ { j } } )$ ; otherwise it is 0. 

(B) Ordinary least squares linear regression. We perform the regression of Y against X and the decision function is $\begin{array} { r } { F _ { B } ( Z _ { S } ) ( X ) = I [ \hat { \beta } _ { Z \mathfrak { c } } ^ { \prime } X > \frac { 1 } { \gamma } ] } \end{array}$ where $\hat { \beta } _ { S }$ is the ordinary least squares regression coefficient estimates<sup>11</sup> obtained by training on the set $Z _ { S }$ . Thus $L _ { B } ( j , i ) = I [ F _ { B } ( Z _ { S _ { i } } ) ( X _ { i } ) \neq Y _ { i } ]$ is equal to 1 whenever this algorithm misclassifies example i when the training set is $Z _ { S _ { j } }$ ; otherwise it is 0. 

On top of inference about the generalization errors $n _ { 1 } \mu _ { A }$ and ${ } n _ { 1 } \mu _ { B }$ associated with those two algorithms, we also consider inference about $\ L _ { n _ { 1 } } \mu _ { A - B } = \ L _ { n _ { 1 } } \mu _ { A } - \ L _ { n _ { 1 } } \mu _ { B } =$ $E [ L _ { A - B } ( j , i ) ]$ where $L _ { A - B } ( j , i ) = L _ { A } ( j , i ) - L _ { B } ( j , i ) .$ 

Table 3 describes the four simulations we performed for the Gaussian populations classification problem. Again, we considered two simulations with $n = 2 0 0$ and two simulations with $n = 2 0 0 0$ . We also chose the parameters $\mu _ { 0 } , \mu _ { 1 } , \Sigma _ { 0 }$ and $\Sigma _ { 1 }$ in such a way that in Simulations 2 and 4, the two algorithms generalize equally well; in Simulations 1 and 3, the linear regression generalizes better than the regression tree. The table also provides some summary confidence intervals for quantities of interest, namely ${ } n _ { 1 } \mu { } ,$ $\begin{array} { r } { \rho ( n _ { 1 } , n _ { 2 } ) = \frac { \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } ) } { \sigma _ { 1 } ( n _ { 1 } , n _ { 2 } ) } } \end{array}$ and $r .$ 


Table 3. Description of four simulations for the classification of two Gaussian populations.


<table><tr><td></td><td>Simulation 1</td><td>Simulation 2</td><td>Simulation 3</td><td>Simulation 4</td></tr><tr><td>n</td><td>200</td><td>200</td><td>2000</td><td>2000</td></tr><tr><td><eq>\mu_0</eq></td><td>(0,0)</td><td>(0,0)</td><td>(0,0)</td><td>(0,0)</td></tr><tr><td><eq>\mu_1</eq></td><td>(1,1)</td><td>(1,1)</td><td>(1,1)</td><td>(1,1)</td></tr><tr><td><eq>\Sigma_0</eq></td><td><eq>I_2</eq></td><td><eq>I_2</eq></td><td><eq>I_2</eq></td><td><eq>I_2</eq></td></tr><tr><td><eq>\Sigma_1</eq></td><td><eq>\frac{1}{2}I_2</eq></td><td><eq>\frac{1}{6}I_2</eq></td><td><eq>\frac{1}{2}I_2</eq></td><td><eq>0.173I_2</eq></td></tr><tr><td><eq>_{n/2}\mu_{A^*}</eq></td><td>[0.249,0.253]</td><td>[0.146,0.149]</td><td>[0.247,0.248]</td><td>[0.142,0.143]</td></tr><tr><td><eq>_{n/2}\mu_B</eq></td><td>[0.204,0.208]</td><td>[0.146,0.148]</td><td>[0.200,0.201]</td><td>[0.142,0.143]</td></tr><tr><td><eq>_{n/2}\mu_{A-B^*}</eq></td><td>[0.044,0.046]</td><td>[-0.001,0.002]</td><td>[0.0467,0.0475]</td><td><eq>[-1\times 10^{-4},8\times 10^{-4}]</eq></td></tr><tr><td><eq>_{9n/10}\mu_{A^*}</eq></td><td>[0.247,0.252]</td><td>[0.142,0.147]</td><td>[0.235,0.237]</td><td>[0.132,0.133]</td></tr><tr><td><eq>_{9n/10}\mu_B</eq></td><td>[0.201,0.205]</td><td>[0.142,0.145]</td><td>[0.199,0.200]</td><td>[0.142,0.143]</td></tr><tr><td><eq>_{9n/10}\mu_{A-B^*}</eq></td><td>[0.044,0.049]</td><td>[-0.001,0.003]</td><td>[0.036,0.037]</td><td>[-0.011,-0.009]</td></tr><tr><td><eq>\rho_A(\frac{n}{2},\frac{n}{2})</eq></td><td>[0.345,0.392]</td><td>[0.392,0.438]</td><td>[0.354,0.400]</td><td>[0.380,0.423]</td></tr><tr><td><eq>\rho_B(\frac{n}{2},\frac{n}{2})</eq></td><td>[0.418,0.469]</td><td>[0.369,0.417]</td><td>[0.462,0.508]</td><td>[0.388,0.432]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2},\frac{n}{2})</eq></td><td>[0.128,0.154]</td><td>[0.174,0.205]</td><td>[0.120,0.146]</td><td>[0.179,0.211]</td></tr><tr><td><eq>\rho_A(\frac{n}{2},\frac{n}{10})</eq></td><td>[0.189,0.223]</td><td>[0.224,0.260]</td><td>[0.190,0.225]</td><td>[0.207,0.242]</td></tr><tr><td><eq>\rho_B(\frac{n}{2},\frac{n}{10})</eq></td><td>[0.150,0.182]</td><td>[0.135,0.163]</td><td>[0.141,0.170]</td><td>[0.129,0.156]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2},\frac{n}{10})</eq></td><td>[0.100,0.124]</td><td>[0.130,0.157]</td><td>[0.087,0.106]</td><td>[0.112,0.138]</td></tr><tr><td><eq>\rho_A(\frac{9n}{10},\frac{n}{10})</eq></td><td>[0.137,0.166]</td><td>[0.156,0.187]</td><td>[0.113,0.137]</td><td>[0.126,0.153]</td></tr><tr><td><eq>\rho_B(\frac{9n}{10},\frac{n}{10})</eq></td><td>[0.089,0.112]</td><td>[0.077,0.097]</td><td>[0.080,0.102]</td><td>[0.081,0.100]</td></tr><tr><td><eq>\rho_{A-B}(\frac{9n}{10},\frac{n}{10})</eq></td><td>[0.077,0.096]</td><td>[0.090,0.111]</td><td>[0.049,0.065]</td><td>[0.078,0.100]</td></tr><tr><td><eq>r_A</eq></td><td>[0.007,0.018]</td><td>[0.025,0.039]</td><td>[-0.005,0.003]</td><td>[-0.003,0.006]</td></tr><tr><td><eq>r_B</eq></td><td>[0.006,0.017]</td><td>[0.023,0.037]</td><td>[-0.003,0.007]</td><td>[-0.003,0.006]</td></tr><tr><td><eq>r_{A-B}</eq></td><td>[0.010,0.021]</td><td>[0.007,0.017]</td><td>[-0.003,0.006]</td><td>[-0.001,0.009]</td></tr></table>

In each of the four simulations, 1000 independent samples of size n where generated with µ<sub>0</sub>, $\mu _ { 1 } , \Sigma _ { 0 } , \Sigma _ { 1 }$ as shown in the table. 95% confidence intervals for $\begin{array} { r } { n _ { 1 } \mu , \rho ( n _ { 1 } , n _ { 2 } ) = \frac { \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } ) } { \sigma _ { 1 } ( n _ { 1 } ) } \text{and} r = \operatorname{Corr} [ ( \hat { \mu } _ { ( m ) } - \hat { \mu } _ { ( m ) } ^ { c } ) ^ { 2 } , ( \hat { \mu } _ { ( m ^ { \prime } ) } - \hat { \mu } _ { ( m ^ { \prime } ) } ^ { c } ) ^ { 2 } ] } \end{array}$ defined after (11) are provided The subscripts <sub>A</sub>, <sub>B</sub> and $A - B$ indicates whether we are working with $L _ { A } , L _ { B }$ or $L _ { A - B } .$ 

An asterisk besides $\mu$ indicates that powers of tests for tha ${ } , \mu$ are displayed in a figure. 

3. Classification of letters. We consider the problem of estimating generalization errors in the Letter Recognition classification problem (Blake, Keogh, & Merz, 1998). The learning algorithms are 

(A) Classification tree. We train a classification tree (Breiman et al., $1 9 8 4 ) ^ { 1 2 }$ to obtain its decision function $F _ { A } ( Z _ { S } ) ( \boldsymbol { X } )$ . Here the classification loss function $L _ { A } ( j , i ) =$ $I [ F _ { A } ( Z _ { S _ { i } } ) ( X _ { i } ) \neq Y _ { i } ]$ is equal to 1 whenever this algorithm misclassifies example i when the training set is $Z _ { S _ { i } ; }$ otherwise it is 0. 

(B) First nearest neighbor. We apply the first nearest neighbor rule with a distorted distance metric to pull down the performance of this algorithm to the level of the classification tree (as in Dietterich (1998)). Specifically, the distance between two vectors of inputs $X ^ { ( 1 ) }$ and $X ^ { ( 2 ) }$ is 

$$
d \big (X ^ {(1)}, X ^ {(2)} \big) = \sum_ {k = 1} ^ {3} w ^ {2 - k} \sum_ {i \in C _ {k}} \big (X _ {i} ^ {(1)} - X _ {i} ^ {(2)} \big) ^ {2}
$$

where $C _ { 1 } = \{ 1 , 3 , 9 , 1 6 \} , C _ { 2 } = \{ 2 , 4 , 6 , 7 , 8 , 1 0 , 1 2 , 1 4 , 1 5 \}$ and $C _ { 3 } = \{ 5 , 1 1 , 1 3 \}$ denote the sets of components that are weighted by w, 1 and $w ^ { - 1 }$ respectively. Table 4 shows the values of w considered. We have $L _ { B } ( j , i )$ equal to 1 whenever this algorithm misclassifies example i when the training set is $Z _ { S _ { j } }$ ; otherwise it is 0. 

In addition to inference about the generalization errors $n _ { 1 } \mu _ { A }$ and ${ } n _ { 1 } \mu _ { B }$ associated with those two algorithms, we also consider inference about $\ L _ { n _ { 1 } } \mu _ { A - B } = \ L _ { n _ { 1 } } \mu _ { A } - \ L _ { n _ { 1 } } \mu _ { B } =$ $E [ L _ { A - B } ( j , i ) ]$ where $L _ { A - B } ( j , i ) = L _ { A } ( j , i ) - L _ { B } ( j , i )$ . We sample, without replacement, 300 examples from the 20000 examples available in the Letter Recognition data base. Repeating this 1000 times, we obtain 1000 sets of data of the form $\{ Z _ { 1 } , \ldots , Z _ { 3 0 0 } \}$ The table also provides some summary confidence intervals for quantities of interest, namely $\begin{array} { r } { { \bf \Phi } _ { n _ { 1 } } \mu , \rho ( n _ { 1 } , n _ { 2 } ) = \frac { \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } ) } { \sigma _ { 1 } ( n _ { 1 } , n _ { 2 } ) } } \end{array}$ and r. 

Before we comment on Tables 2–4, let us describe how the confidence intervals shown in those tables were obtained. These intervals are not the confidence intervals computed from the statistics in Section 4: the latter can be computed on a single data set $Z_1^n$, whereas the table intervals use 1000 independent data sets. For each data set, ${}_{n_1}^{n_2}\hat{\mu}_{25}$ is the average of 25 crude estimates and has expectation ${}_{n_1}\mu$. The crude estimates have the moment structure of Lemma 1, with $\beta={}_{n_1}\mu$ and $\pi=\rho(n_1,n_2)=\sigma_2(n_1,n_2)/\sigma_1(n_1,n_2)$. Thus the 1000 data sets provide 1000 independent instances of $\vec{\mu}=(\hat{\mu}_1,\ldots,\hat{\mu}_{25})'$. As shown in Appendix A.3, estimating-function theory (White, 1982) then yields approximate confidence intervals for ${}_{n_1}\mu$ and $\rho(n_1,n_2)$. Confidence intervals for the correlation $r$ defined after (11) are obtained in the same way, using 1000 independent instances of the vector of the 20 squared split differences. The $\hat{\mu}_{(m)}$ and $\hat{\mu}_{(m)}^c$ in those differences are ${}_{2n/5}^{n/10}\hat{\mu}_{15}$ estimators, since we advocate $J=15$ later in this section.


Table 4. Description of six simulations for the letter recognition problem.


<table><tr><td></td><td>Simulation 1</td><td>Simulation 2</td><td>Simulation 3</td></tr><tr><td>n</td><td>300</td><td>300</td><td>300</td></tr><tr><td>w</td><td>1</td><td>5</td><td>10</td></tr><tr><td><eq>n/2\mu_{B^*}</eq></td><td>[0.539, 0.542]</td><td>[0.593, 0.596]</td><td>[0.632, 0.635]</td></tr><tr><td><eq>n/2\mu_{A-B^*}</eq></td><td>[0.150, 0.152]</td><td>[0.096, 0.099]</td><td>[0.057, 0.060]</td></tr><tr><td><eq>9n/10\mu_B</eq></td><td>[0.434, 0.439]</td><td>[0.496, 0.501]</td><td>[0.544, 0.548]</td></tr><tr><td><eq>9n/10\mu_{A-B^*}</eq></td><td>[0.148, 0.153]</td><td>[0.086, 0.091]</td><td>[0.039, 0.044]</td></tr><tr><td><eq>\rho_B(\frac{n}{2}, \frac{n}{2})</eq></td><td>[0.310, 0.355]</td><td>[0.334, 0.376]</td><td>[0.349, 0.393]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2}, \frac{n}{2})</eq></td><td>[0.134, 0.160]</td><td>[0.152, 0.180]</td><td>[0.160, 0.191]</td></tr><tr><td><eq>\rho_B(\frac{n}{2}, \frac{n}{10})</eq></td><td>[0.167, 0.198]</td><td>[0.182, 0.214]</td><td>[0.197, 0.232]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2}, \frac{n}{10})</eq></td><td>[0.122, 0.148]</td><td>[0.129, 0.155]</td><td>[0.130, 0.156]</td></tr><tr><td><eq>\rho_B(\frac{9n}{10}, \frac{n}{10})</eq></td><td>[0.105, 0.129]</td><td>[0.106, 0.131]</td><td>[0.115, 0.140]</td></tr><tr><td><eq>\rho_{A-B}(\frac{9n}{10}, \frac{n}{10})</eq></td><td>[0.085, 0.105]</td><td>[0.085, 0.105]</td><td>[0.084, 0.104]</td></tr><tr><td><eq>r_B</eq></td><td>[-0.006, 0.001]</td><td>[-0.004, 0.004]</td><td>[-0.004, 0.005]</td></tr><tr><td><eq>r_{A-B}</eq></td><td>[-0.004, 0.004]</td><td>[-0.004, 0.004]</td><td>[-0.003, 0.005]</td></tr><tr><td></td><td>Simulation 4</td><td>Simulation 5</td><td>Simulation 6</td></tr><tr><td>n</td><td>300</td><td>300</td><td>300</td></tr><tr><td>w</td><td>17.25</td><td>25</td><td>2048</td></tr><tr><td><eq>n/2\mu_{B^*}</eq></td><td>[0.666, 0.669]</td><td>[0.690, 0.693]</td><td>[0.779, 0.782]</td></tr><tr><td><eq>n/2\mu_{A-B^*}</eq></td><td>[0.023, 0.026]</td><td>[-0.001, 0.002]</td><td>[-0.089, -0.087]</td></tr><tr><td><eq>9n/10\mu_B</eq></td><td>[0.586, 0.591]</td><td>[0.616, 0.620]</td><td>[0.730, 0.734]</td></tr><tr><td><eq>9n/10\mu_{A-B^*}</eq></td><td>[-0.003, 0.001]</td><td>[-0.033, -0.028]</td><td>[-0.147, -0.142]</td></tr><tr><td><eq>\rho_B(\frac{n}{2}, \frac{n}{2})</eq></td><td>[0.360, 0.404]</td><td>[0.368, 0.413]</td><td>[0.347, 0.392]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2}, \frac{n}{2})</eq></td><td>[0.167, 0.198]</td><td>[0.170, 0.202]</td><td>[0.178, 0.211]</td></tr><tr><td><eq>\rho_B(\frac{n}{2}, \frac{n}{10})</eq></td><td>[0.200, 0.238]</td><td>[0.201, 0.238]</td><td>[0.201, 0.237]</td></tr><tr><td><eq>\rho_{A-B}(\frac{n}{2}, \frac{n}{10})</eq></td><td>[0.130, 0.156]</td><td>[0.129, 0.155]</td><td>[0.133, 0.162]</td></tr><tr><td><eq>\rho_B(\frac{9n}{10}, \frac{n}{10})</eq></td><td>[0.118, 0.143]</td><td>[0.125, 0.151]</td><td>[0.119, 0.145]</td></tr><tr><td><eq>\rho_{A-B}(\frac{9n}{10}, \frac{n}{10})</eq></td><td>[0.085, 0.106]</td><td>[0.087, 0.108]</td><td>[0.094, 0.116]</td></tr><tr><td><eq>r_B</eq></td><td>[-0.004, 0.004]</td><td>[-0.005, 0.004]</td><td>[0.002, 0.012]</td></tr><tr><td><eq>r_{A-B}</eq></td><td>[-0.002, 0.007]</td><td>[-0.001, 0.009]</td><td>[-0.001, 0.009]</td></tr></table>


In each of the six simulations, 1000 independent samples of size $n=300$ were generated, and Algorithms A and B were used, with B using the distorted metric factor $w$ shown in the table. The table provides 95% confidence intervals for ${}_{n_1}\mu$, $\rho(n_1,n_2)=\sigma_2(n_1,n_2)/\sigma_1(n_1,n_2)$, and the correlation $r$ defined after (11).



The subscripts $A \bullet B$ and $A - B$ indicates whether we are working with $L _ { A } , L _ { B }$ or $L _ { A - B } .$ 



An asterisk besides µ indicates that powers of tests for that µ are displayed in a figure. See Table 5 for the results obtained with Algorithm A (the same for all 6 simulations). 



Table 5. Confidence intervals for the statistics measured with Algorithm A for all 6 simulations with the letter recognition problem (see Table 4).


<table><tr><td><eq>_{n/2}\mu_{A}</eq></td><td><eq>_{9n/10}\mu_{A}</eq></td><td><eq>\rho_{A}(\frac{n}{2},\frac{n}{2})</eq></td><td><eq>\rho_{A}(\frac{n}{2},\frac{n}{10})</eq></td><td><eq>\rho_{A}(\frac{9n}{10},\frac{n}{10})</eq></td><td><eq>r_{A}</eq></td></tr><tr><td>[0.691, 0.694]</td><td>[0.585, 0.589]</td><td>[0.223, 0.259]</td><td>[0.137, 0.164]</td><td>[0.099, 0.123]</td><td>[0.002, 0.013]</td></tr></table>

We see that $n _ { 1 } \mu$ may substantially differ for different $n _ { 1 } .$ . This is most evident in Table 4 where confidence intervals for $1 5 0 \mu$ differ from confidence intervals for ${}_{270}\mu in a noticeable manner. We see that our very naive approximation $\begin{array} { r } { \rho _ { 0 } ( n _ { 1 } , n _ { 2 } ) = \frac { n _ { 2 } } { n _ { 1 } + n _ { 2 } } } \end{array}$ is not as bad as one could expect. Often the confidence intervals for the actual $\rho ( n _ { 1 } , n _ { 2 } )$ contains $\rho _ { 0 } ( n _ { 1 } , n _ { 2 } ) . ^ { 1 3 }$ When this is not the case, the approximation $\rho _ { 0 } ( n _ { 1 } , n _ { 2 } )$ usually appears to be reasonably close to the actual value of the correlation $\rho ( n _ { 1 } , n _ { 2 } )$ . Furthermore, when we compare two algorithms, the approximation $\rho _ { 0 } ( n _ { 1 } , n _ { 2 } )$ is not smaller than the actual value of the correlation $\rho _ { A - B } ( n _ { 1 } , n _ { 2 } )$ , which is good since that indicates that the inference based on the corrected pseudo-bootstrap and on the corrected resampled t-test will not be liberal, as argued in Section 4. We finally note that the correlation r appears to be fairly small, except when we compare algorithms A and B in the simple linear regression problem. Thus, as we stated at the end of Section 3, we should expect Var[ $\mathbf { \Sigma } _ { n _ { 1 } ^ { \prime } } ^ { n _ { 2 } } \hat { \sigma } _ { J } ^ { 2 } ]$ to decrease like $\textstyle { \frac { 1 } { M } }$ 

## 5.1. Sizes and powers of tests

One of the most important thing to investigate is the size (probability of rejecting the null hypothesis when it is true) of the tests based on the statistics shown in Section 4 and compare their powers (probability of rejecting the null hypothesis when it is false). The four panels of figure 1 show the estimated powers of the statistics for the hypothesis $H _ { 0 } \colon { } _ { n / 2 } \mu _ { A } = \mu _ { 0 }$ for various values of $\mu _ { 0 }$ in the regression problem. We estimate powers (probabilities of rejection) by proportions of rejection observed in the simulation. We must underline that, despite appearances, these are not “power curves” in the usual sense of the term (see Appendix $\mathbf { A } ) .$ In a “power curve”, the hypothesized value of $n / 2 \mu _ { A }$ is fixed and the actual value of $n / 2 \mu _ { A }$ varies. Here, it is the reverse that we see in a given panel: the actual value of ${ } n / 2 { \mu } _ { A }$ is fixed while the hypothesized value of $_ { n / 2 } \mu _ { A } \ ( \mathbf { i . e . \ } \mu _ { 0 } )$ is varied. We may call this a pseudo-power curve. We do this because constructing “power curves” would be too computationally expensive. Nevertheless, pseudo-power curves shown in figure 1 convey information similar to conventional “power curves”. Indeed, we can find the size of a test by reading its pseudo-power curve at the actual value of $n / 2 \mu _ { A }$ (laying between the two vertical dotted lines). We can also appreciate the progression of the power as the hypothesized value of $n / 2 \mu _ { A }$ and the actual value of $n / 2 \mu _ { A }$ grow apart. We shall see in figure 7 that those pseudo-power curves are good surrogate to “power curves”. 

Figures 2 through 6 are counterparts of figure 1 for other problems and/or algorithms. Power plots corresponding to tests about ${ n / 2 } { \mu } _ { B }$ in the regression problem and about ${ n / 2 } { \mu } _ { B }$ in the classification of Gaussian populations problem are not shown since they convey the same information as figure 1. However, missing figures are available in Nadeau and Bengio (1999). 

![Figure 1](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/94d0c0171a0f3329dcae370a069edefe917720f0309479f579ffb2afd67d5a88.jpg)



Figure 1. Powers of the tests about $H _ { 0 } \colon {}_{n/2}\mu_A = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu_0$ for the regression problem. Each panel corresponds to one of the simulations design described in Table 2. The dotted vertical lines correspond to the 95% confidence interval for the actual ${ \frac { n } { 2 } } \mu _ { A }$ shown in Table 2, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). Where it matters J = 15, M = 10 and $R=15$ were used.


Note that in order to reduce the number of displayed line types in figure 1 and its counterparts appearing later, some curves share the same line type. So one must take note of the following. 

- In a given panel, you will see four solid curves. They correspond to either the resampled t-test or the corrected resampled t-test with $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } \operatorname { o r } n _ { 2 } = \frac { n } { 2 } } \end{array}$ . Curves with circled points correspond to $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ (40% thrown away); curves without circled points correspond to $\begin{array} { r } { n _ { 2 } = \frac { n } { 2 } } \end{array}$ . Telling apart the resampled t-test and the corrected resampled t-test is easy; the two curves that are well above all others correspond to the resampled t-test. 

- The dotted curves depict the conservative Z test with either $\textstyle n _ { 2 } = { \frac { n } { 1 0 } }$ (when it is circled) or $\begin{array} { r } { n _ { 2 } = \frac { n } { 2 } } \end{array}$ (when it is not circled). 

- You might have noticed that the pseudo-bootstrap and the corrected pseudo-bootstrap do not appear in figure 1 and all its counterparts (except figures 3 and 4). We ignored them because, as we anticipated from political ratios shown in Table 1, the pseudo-bootstrap test behaves like the resampled t-test and the corrected pseudo-bootstrap test behaves like the corrected resampled t-test. If we don’t ignore the pseudo-bootstrap, some figures become too crowded. We made an exception and plotted curves corresponding to the pseudo-bootstrap in figures 3 and 4. In those two figures, the pseudo-bootstrap and corrected pseudo-bootstrap curves are depicted with solid curves (just like the resampled t-test and corrected resampled t-test) and obey the same logic that applies to resampled t-test and corrected resampled t-test curves. What you must notice is that these figures look like the others except that where you would have seen a single solid curve, you now see two solid curves that nearly overlap. That shows how similar the resampled t-test and the pseudo-bootstrap are. This similitude is present for all problems, no just for the inference about ${ \ L } _ { \frac { n } { 2 } } ^ { n } \mu _ { A } \ \mathrm { o r } \quad { \ L } _ { \frac { n } { 2 } } ^ { n } \mu _ { A - B }$ in the classification of Gaussian populations (figures 3 and 4). We chose to show the pseudo-bootstrap curves in figures 3 and 4 because this is where the plots looked the least messy when the pseudo-bootstrap curves were added. 

![Figure 2](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/dd0672f8b35934d26d12439b6b4a46bd81e5a892c673be45227fc3f0cc61a03f.jpg)



Figure 2. Powers of the tests about $H _ { 0 } \colon {}_{n/2}\mu_{A-B} = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu_0$ for the regression problem. Each panel corresponds to one of the simulations design described in Table 2. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{n/2}\mu_{A-B}$ shown in Table 2, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). Where it matters J = 15, M = 10 and R = 15 were used.


![Figure 3](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/fa45341d9e2fb102cac089a7c0391084dc1a5452e4942a172a0bed36a12b537a.jpg)



Figure 3. Powers of the tests about $H _ { 0 } \colon {}_{n/2}\mu_A = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu _ { 0 }$ for the classification of Gaussian populations problem. Each panel corresponds to one of the simulations design described in Table 3. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{n/2}\mu_A$ shown in Table 3, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). Where it matters J = 15, M = 10 and $R=15$ were used.


Here’s what we can draw from those figures. 

- The most striking feature of those figures is that the actual size of the resampled t-test and the pseudo-bootstrap procedure are far away from the nominal size 10%. This is what we expected in Section 4. The fact that those two statistics are more liberal when $\begin{array} { r } { n _ { 2 } = \frac { n } { 2 } } \end{array}$ than they are when $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ (40% of the data thrown away) suggests that $\rho ( n _ { 1 } , n _ { 2 } )$ is increasing in $n _ { 2 }$ . This is in line with what one can see in Tables 2–4, and the simple approximation $\begin{array} { r } { \rho _ { 0 } ( n _ { 1 } , n _ { 2 } ) = \frac { n _ { 2 } } { n _ { 1 } + n _ { 2 } } } \end{array}$ 

- We see that the sizes of the corrected resampled t-test (and corrected pseudo-bootstrap) are in line with what we could have forecasted from Tables 2–4. Namely the test is liberal when $\rho ( n _ { 1 } , n _ { 2 } ) > \rho _ { 0 } ( n _ { 1 } , n _ { 2 } )$ , conservative when $\rho ( n _ { 1 } , n _ { 2 } ) < \rho _ { 0 } ( n _ { 1 } , n _ { 2 } )$ , and pretty much on target when $\rho ( n _ { 1 } , n _ { 2 } )$ does not differ significantly from $\rho _ { 0 } ( n _ { 1 } , n _ { 2 } )$ . For instance, on figure 1 the sizes of the corrected resampled t-test are close to the nominal 10%. We see in Table 2 that $\rho _ { A } ( n _ { 1 } , n _ { 2 } )$ does not differ significantly from $\rho _ { 0 } ( n _ { 1 } , n _ { 2 } )$ . Similarly, in figures 3 and 5, the corrected resampled t-test appears to be significantly liberal when $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ (40% of the data thrown away).<sup>14</sup> We see that $\rho _ { A } ( { \frac { n } { 2 } } , { \frac { n } { 1 0 } } )$ is significantly greater than $\begin{array} { r } { \rho _ { 0 } ( \frac { n } { 2 } , \frac { n } { 1 0 } ) = \frac { 1 } { 6 } } \end{array}$ in Table 3, and $\rho _ { B } ( { \frac { n } { 2 } } , { \frac { n } { 1 0 } } )$ is significantly greater than $\begin{array} { r } { \rho _ { 0 } ( \frac { n } { 2 } , \frac { n } { 1 0 } ) = \frac { 1 } { 6 } } \end{array}$ in Table 4. However, in those same figures, we see that the corrected resampled t-test that do not throw data away is conservative and, indeed, we can see that $\rho _ { A } { \bigl ( } { \frac { n } { 2 } } , { \frac { n } { 2 } } { \bigr ) }$ is significantly smaller than $\begin{array} { r } { \rho _ { 0 } ( \frac { n } { 2 } , \frac { n } { 2 } ) = \frac { 1 } { 2 } } \end{array}$ in Table 3, and $\rho _ { B } { \bigl ( } { \frac { n } { 2 } } , { \frac { n } { 2 } } { \bigr ) }$ is significantly smaller than $\begin{array} { r } { \rho _ { 0 } ( \frac { n } { 2 } , \frac { n } { 2 } ) = \frac { 1 } { 2 } } \end{array}$ in Table 4. 

![Figure 4](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/fa678d3e8a03c5ddf58016f5d3452e9c338cf1f7944c26aa3130966f415cebc1.jpg)



Figure 4. Powers of the tests about $H _ { 0 } \colon {}_{n/2}\mu_{A-B} = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu_0$ for the classification of Gaussian populations problem. Each panel corresponds to one of the simulations design described in Table 3. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{n/2}\mu_{A-B}$ shown in Table 3, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). Where it matters J = 15, M = 10 and $R=15$ were used.


- The conservative Z with $\begin{array} { l l l } { n _ { 2 } ~ = ~ { \frac { n } { 2 } } } \end{array}$ is too conservative. However, when $\begin{array} { l } { n _ { 2 } ~ = ~ \frac { n } { 1 0 } } \end{array}$ (so that $\begin{array} { r } { \frac { n _ { 1 } } { n _ { 2 } } = 5 } \end{array}$ , more in line with normal usage), the conservative Z has more interesting properties. It does not quite live up to its name since it is at times liberal, but barely so. Its size is never very far from 10% (like 20% for instance), making it the best inference procedure among those considered in terms of size. 

![Figure 5](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/5a5bc813256aa867c17132229e1fea55fb55442a836c5c2689bf483e0ad0bac7.jpg)



Figure 5. Powers of the tests about $H _ { 0 } \colon {}_{n/2}\mu_B = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu _ { 0 }$ for the letter recognition problem. Each panel corresponds to one of the simulations design described in Table 4. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{n/2}\mu_B$ shown in Table 4, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). Where it matters $J=15$ , M = 10 and $R=15$ were used.


- The t-test and Dietterich’s $5 \times 2$ cv are usually well behaved in term of size, but they are sometimes fairly liberal as can be seen in some panels of figures 2–5. 

- When their sizes are comparable, the powers of the t-test, Dietterich’s $5 \times 2 \mathrm { c v } ,$ conservative Z throwing out 40% of the data and corrected resampled t-test throwing out 40% of the data are fairly similar. If we have to break the tie, it appears that the t -test is the most powerful, Dietterich’s $5 \times 2 ~ \mathrm { c v }$ is the least powerful procedure and the corrected resampled t-test and the corrected conservative Z lay in between. The fact that the conservative Z and the corrected resampled t-test perform well despite throwing 40% of the data indicates that these methods are very powerful compared to Dietterich’s $5 \times 2$ cv and the t-test. This may be seen in figure 1 where the size of the corrected resampled t-test with the full data is comparable to the size of other tests. The power of the corrected resampled t-test is then markedly superior to the powers of other tests with comparable size. In other figures, we see the power of the corrected resampled t-test with full data and/or conservative Z with full data catch on (as we move away from the null hypothesis) the powers of other methods that have larger size. 

![Figure 6](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/647d74a31da3de38aff39346038c7e0534d72a6f12d5926da30e194a7b674311.jpg)



Figure 6. Powers of the tests about $H _ { 0 } \colon {}_{n/2}\mu_{A-B} = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu _ { 0 }$ for the letter recognition problem. Each panel corresponds to one of the simulations design described in Table 4. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{n/2}\mu_{A-B}$ shown in Table 4, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). Where it matters $J=15$, $M=10$ and $R=15$ were used.


As promised earlier, we now illustrate that pseudo-power curves are good surrogates to actual real power curves. For the letter recognition problem, we have the opportunity to draw real power curves since we have simulated data under six different schemes. Recall from Table 4 that we have simulated data with $1 5 0 \mu B$ approximatively equal to 0.541, 0.595, 0.634, 0.668, 0.692, 0.781 and $1 5 0  { \mu } _ { A - B }$ approximatively equal to $0 . 1 5 1 , 0 . 0 9 8 , 0 . 0 5 9 , 0 . 0 2 5 , 0 . 0 0 1 , - 0 . 0 8 8$ in Simulations 1 through 6 respectively. The circled lines in figure 7 depict real power curves. For instance, in the left panel, the power of tests for $H _ { 0 } \colon \ _ { 1 5 0 } \mu _ { B } = 0 . 6 9 2$ has been obtained in all six simulations, enabling us to draw the circled curves. The non-circled curves correspond to what we have been plotting so far. Namely, in Simulation 5, we computed the powers of tests for $H _ { 0 } \colon \ _ { 1 5 0 } \mu _ { B } = \mu _ { 0 }$ with µ = 0.541, 0.595, 0.634, 0.668, 0.692, 0.781, enabling us to draw the non-circled curves. 

![Figure 7, left panel](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/c420af5509585d7e56244b22e0bc64debfbed0876f40c9ce03470dd1440ee51d.jpg)


![Figure 7, right panel](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/e5e047c839f19033077fefe525611826c3c8321b5bd4020d51af732a68eb8ec3.jpg)



Figure 7. Real power curves (circle lines) and pseudo-power curves (not circled) in the letter recognition problem. In the left panel, we see “real” and “pseudo” power curves for the null hypothesis $H_0: {}_{150}\mu_A$ = 0 . 6 9 2$ . In the right panel, we see “real” and “pseudo” power curves for the null hypothesis $H _ { 0 } \colon _ { 1 5 0 } \mu _ { A - B } = 0 . 0 0 1$ . See the end of Section 5.1 for more details on their constructions. Here, the “corrected resampled t” and the “conservative $Z$” statistic are those which do not throw away data.


We see that circled and non-circled curves agree relatively well, leading us to believe that our previous plots are good surrogates to real power curves. 

## 5.2. The choice of J

In Section 5.1, the statistics involving ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ used $J = 1 5$ . We look at how those statistics behave with varying $J ^ { \prime } \mathbf { s } ,$ , in order to formulate a recommendation on the choice of J . We are going to do so with $\begin{array} { r } { n _ { 1 } = \frac { 9 n } { 1 0 } } \end{array}$ and $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ , which correspond to a more natural usage for these statistics. Of the seven statistics displayed in Section 4 (see also Table 1), five involved ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ . We ignore the pseudo-bootstrap and the corrected pseudo-bootstrap as political ratios provided in Section 4 and empirical evidence in Section 5.1 suggest that these statistics are virtually identical to the resampled t-test and the corrected resampled t-test (but require a lot more computation). We therefore only consider the resampled t-test, the corrected resampled t-test and the conservative Z here. 

The investigation of the properties of those statistics will again revolve around their sizes and powers. You will therefore see that figures in this section (figures 8 to 12) are similar to those of the Section 5.1. Note that figures corresponding to $9 n / 1 0  \mu B$ are not shown as they convey no additional information. However, missing figures are available in Nadeau and Bengio (1999). In a given plot, we see the powers of the three statistics when $J = 5 $ 2 $J = 1 0 , J = 1 5$ and $J = 2 5$ . Therefore a total of twelve curves are present in each plot. 

Here’s what we can draw from those figures. 

- Again, the first thing that we see is that the resampled t-test is very liberal. However, things were even worse in Section 5.1. That is due to the fact that $\rho ( \textstyle { \frac { 9 n } { 1 0 } } , \frac { n } { 1 0 } )$ is smaller than $\rho ( \textstyle { \frac { n } { 2 } } , \frac { n } { 1 0 } )$ and $\rho ( \textstyle { \frac { n } { 2 } } , \frac { n } { 2 } )$ . We also see that the statistic is more liberal when J is large, as it should be according to the theoretical discussion of that statistic in Section 4. 

![Figure 8](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/0d1bf904c951a38ec5188d3235848335772779f45dc0e92e2a311a7a307be609.jpg)



Figure 8. Powers of the tests about $H_0: {}_{9n/10}\mu_A = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu_0$ and J for the regression problem. Each panel corresponds to one of the simulations design described in Table 2. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{9n/10}\mu_A$ shown in Table 2, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (a significance level 5%). For the conservative $Z , M=10$ was used.


- The conservative Z lives up to its name. 

- Regarding the corrected resampled t-test, the plots again only confirm what we might have guessed from Tables 2–4. Namely the resampled t-test is conservative when $\rho ( \textstyle { \frac { 9 \bar { n } } { 1 0 } } , \textstyle { \frac { n } { 1 0 } } )$ is significantly greater than $\rho _ { 0 } ( \frac { 9 n } { 1 0 } , \frac { n } { 1 0 } ) = 0 . 1$ , liberal when $\rho ( \frac { 9 n } { 1 0 } , \frac { n } { 1 0 } )$ is significantly smaller then 0.1, and has size very close to 0.1 otherwise. When it is liberal or conservative, things tend to grow worse when J increases; see figure 10 for the liberal case. That makes sense since the political ratio $\begin{array} { r } { \frac { \operatorname{Var} [ \hat { \mu } ] } { E [ \hat { \sigma } ^ { 2 } ] } = \frac { 1 + J \frac { \rho } { 1 - \rho } } { 1 + J \frac { n _ { 2 } } { n . } } } \end{array}$ (see Table 1) is monotonic in J (increasing when $\textstyle \rho > { \frac { n _ { 2 } } { n _ { 1 } + n _ { 2 } } }$ ; decreasing when $\begin{array} { r } { \rho < \frac { \ddot { n _ { 2 } } ^ { 1 } } { n _ { 1 } + n _ { 2 } } ) } \end{array}$ 

- Obviously (from Eq. (8) or Proposition 2), the greater J is, the greater the power will be. Note that increasing J from 5 to 10 brings about half the improvement in the power obtained by increasing J from 5 to 25. Similarly, increasing J from 10 to 15 brings about half the improvement in the power obtained by increasing J from 10 to 25. With that in mind, we feel that one must take J to be at least equal to 10 as $J = 5$ leads to unsatisfactory power. Going beyond J = 15 gives little additional power and is probably not worth the computational effort. We could tackle this question from a theoretical point of view. We know from (8) that Var[ $\begin{array} { r } { { \bf \Pi } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J } ] = \sigma _ { 1 } ( \rho + \frac { \bar { 1 - \rho } } { J } ) } \end{array}$ . Take $\rho = 0 .$ 1 for instance (that is $\rho _ { 0 } ( \frac { 9 n } { 1 0 } , \frac { n } { 1 0 } ) )$ . Increasing J from 1 to 3 reduces the variance by 60%. Increasing J from 3 to 9 further halves the variance. Increasing J from 9 to ∞ only halves the variance. We thus see that the benefit of increasing J quickly becomes faint. 

![Figure 9](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/f5465e584585e03c4d8c1cfdb5f2c8cc76b5de1a13e617a1c6b6afbd9152ccbc.jpg)



Figure 9. Powers of the tests about $H_0: {}_{9n/10}\mu_{A-B} = \mu _ { 0 }$ at level α = 0.1 for varying $\mu_0$ and J for the regression problem. Each panel corresponds to one of the simulations design described in Table 2. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{9n/10}\mu_{A-B}$ shown in Table 2, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). For the conservative $Z , M=10$ was used.


- Since the conservative Z is fairly conservative, it rarely has the same size as the corrected resampled t-test, making power comparison somewhat difficult. But it appears that the two methods have equivalent powers which makes sense since they are both based on ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { J }$ . We can see this in figures 11 and 12 where the two tests have about the same size and similar power. 

Based on the above observations, we believe that $J = 1 5$ is a good choice: it provides good power with reasonable computational effort. If computational effort is not an issue, one may take $J > 1 5$ , but must not expect a great gain in power. Another reason in favor of not taking J too large is that the size of the resampled t-test gets worse with increasing J when that method is liberal or conservative. 

![Figure 10, panel 1](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/ffc57ef83e914c808389f8c463334b2679b5cedb2494c2298131047caac53dbb.jpg)


![Figure 10, panel 2](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/49f36bb43c041a064bb1447ec243f80edf1e6bb678650ff7fc45a781b9db35ab.jpg)


![Figure 10, panel 3](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/70c22cd16c71ccc1ef6a00e6514d773c89472212b760502132e03251375a08ae.jpg)


![Figure 10, panel 4](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/28184f1e94cd55ae98fb19a95793b6896f7b2f1133440f0488301bcf0f6c71cb.jpg)


![Figure 10, panel 5](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/66b3ca79405c9d8f12d78603b34a0aef39a0662bc023e645d4e6cd06eab5151a.jpg)



Figure 10. Powers of the tests about $H _ { 0 } \colon {}_{9n/10}\mu_A = \mu _ { 0 }$ at level α = 0.1 for varying $\mu _ { 0 }$ and J for the classification of Gaussian populations problem. Each panel corresponds to one of the simulations design described in Table 3. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{9n/10}\mu_A$ shown in Table 3, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). For the conservative Z $M=10$ was used.


Of course the choice of $J$ is not totally independent of $n _ { 1 }$ and $n _ { 2 }$ . Indeed, if one uses a larger test set (and thus a smaller train set), then we might expect $\rho$ to be larger and therefore $J = 1 0$ might then be sufficiently large. 

Although it is not related to the choice of $^ { J , }$ we may comment on the choice of the inference procedure as figures in this section are the most informative in that regard. If one wants an inference procedure that is not liberal, the obvious choice is the conservative $Z .$ However, if one prefers an inference procedure with size close to the nominal size $\alpha$ and is ready to accept departures in the liberal side as well as in the conservative side, then the corrected resampled t appears to be a good choice. However, as we shall see shortly, we can make the conservative $Z$ more or less conservative by playing with M. The advantage of the corrected resampled t is that it requires little computing in comparison to the conservative Z . 

![Figure 11, panel 1](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/96efe5d789abffaa56b3b6027bbd7e290da554e0c16c58727b33c4b383527805.jpg)


![Figure 11, panel 2](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/eda78b690d5f20ea8e86b5e635ec397ac2e4fba4d93abc5c39855b638da26797.jpg)


![Figure 11, panel 3](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/dfd69cad69df788e35a7787bc2f7eb01dcadd54e0c5d71efa8ac0ea7bcdb8e38.jpg)


![Figure 11, panel 4](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/e3824d9f81a078ce1c5e54e6d2f55feabacff9b253110e1cd4966533c7d64ded.jpg)


![Figure 11, panel 5](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/db6326c72ad76f270dc15a670eb00999b51e12cac46a8de93474fc108ce90615.jpg)



Figure 11. Powers of the tests about $H_0: {}_{9n/10}\mu_{A-B} = \mu _ { 0 }$ at level α = 0.1 for varying $\mu_0$ and J for the classification of Gaussian populations problem. Each panel corresponds to one of the simulations design described in Table 3. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{9n/10}\mu_{A-B}$ shown in Table 3, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). For the conservative Z, M = 10 was used.


Finally, we assessed to what extent the pseudo-power curves shown in figures 8 through 12 are good surrogates to actual real power curves. The counterpart of figure 7, not shown here but available in Nadeau and Bengio (1999), shows again that the two types of curves agree well. 

## 5.3. The choice of M

When using the conservative Z, we have so far always used $M = 1 0$ . We study the behavior of this statistic for various values of M in order to formulate a recommendation on the choice of M. Again we consider the case where $\begin{array} { r } { n _ { 1 } = \frac { 9 n } { 1 0 } } \end{array}$ and $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ . The investigation will again revolve around the size and power of the statistic. We see in figure 13 (figures for other problems and/or algorithms convey the same information and are therefore not shown but are available in Nadeau and Bengio (1999)) that the conservative Z is more conservative when M is large. We see that there is not a great difference in the behavior of the conservative 

![Figure 12, panel 1](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/6c5623717f9021857bac8a19b1fdfacc1512f346c1a8343e004253e9e076bb75.jpg)


![Figure 12, panel 2](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/2d5abd6c7bb82c6d53c5ce08ed09f6df841723ec88fcae8f4755a0dde62013c4.jpg)


![Figure 12, panel 3](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/a211784d0ae6e811179d00d97b9989a217fd42f28b620a7f9f2395d49a5bb236.jpg)


![Figure 12, panel 4](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/3c9930fa17b3e69e33e83988c634a46a49ccd76d3328c78cad15b98ca9994e39.jpg)



Figure 12. Powers of the tests about $H _ { 0 } \colon {}_{9n/10}\mu_{A-B} = \mu _ { 0 }$ at level $\alpha = 0 . 1$ for varying $\mu _ { 0 }$ and J for the letter recognition problem. Each panel corresponds to one of the simulations design described in Table 4. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{9n/10}\mu_{A-B}$ shown in Table 4, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%). For the conservative $Z , M = 1 0$ was used.


Z when $M = 1 0$ and when $M = 2 0 .$ . For that reason, we recommend using $M \leq 1 0$ . The difference between $M = 1 0$ and $M = 5$ is more noticeable, $M = 5$ leads to inference that is less conservative, which is not a bad thing considering that with $M = 1 0$ it tends to be a little bit too conservative. With $M = 5$ , the conservative Z is sometimes liberal, but barely so. Using $M < 5$ would probably go against the primary goal of the statistic, that is provide inference that is not liberal. Thus $5 \leq M \leq 1 0$ appears to be a reasonable choice. Within this range, pick M large if non-liberal inference is important; otherwise take M small if you want the size of the test to be closer to the nominal size α (you then accept the risk of performing inference that could be slightly liberal). Of course, computational effort is linear in M so that taking M small has an additional appeal. 

## 6. Conclusion

We have tackled the problem of estimating the variance of the cross-validation estimator of the generalization error. In this paper, we paid special attention to the variability introduced by the selection of a particular training set, whereas most empirical applications of machine learning methods concentrate on estimating the variability of the estimate of generalization error due to the finite test set. 

![Figure 13](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/37a11446-14ca-4e81-8876-9f02768bc154/3d06bcc2943880464d629451c08ce0e4614397c9951d12d649f51f15f2a6d708.jpg)



Figure 13. Powers of the conservative Z (with J = 15) about $H _ { 0 } \colon {}_{9n/10}\mu_{A-B} = \mu _ { 0 }$ at level $\alpha=0.1$ for varying µ and M for the regression problem. Each panel corresponds to one of the simulations design described in Table 2. The dotted vertical lines correspond to the 95% confidence interval for the actual ${}_{9n/10}\mu_{A-B}$ shown in Table 2, therefore that is where the actual size of the tests may be read. The solid horizontal line displays the nominal size of the tests, i.e. 10%. Estimated probabilities of rejection laying above the dotted horizontal line are significantly greater than 10% (at significance level 5%).


A theoretical investigation of the variance to be estimated shed some valuable insight on reasons why some estimators currently in use underestimate the variance. We showed that no general unbiased estimator of the variance of our particular cross-validation estimator could be found. This analysis allowed us to construct two variance estimates that take into account both the variability due to the choice of the training sets and the choice of the test examples. One of the proposed estimators looks like the $5 \times 2$ cv method (Dietterich, 1998) and is specifically designed to overestimate the variance to yield conservative inference. The other may overestimate or underestimate the real variance, but is typically not too far off the target. 

We performed a simulation where the new techniques put forward were compared to test statistics currently used in the machine learning community. We tackle both the inference for the generalization error of an algorithm and the comparison of the generalization errors of two algorithms. We considered two kinds of problems: classification and regression. Various algorithms were considered: linear regression, regression trees, classification trees and the nearest neighbor algorithm. Over this wide range of problems and algorithms, we found that the new tests behave better in terms of size and have powers that are unmatched by any known techniques (with comparable size). 

The simulation also allowed us to recommend values for the parameters involved in the proposed techniques, namely J around 15 and (for the conservative $Z )$ M between 5 and 10. If one wants an inference procedure that is not liberal, the natural choice is the conservative $Z .$ . However, if one prefers an inference procedure with size close to the nominal size α and is ready to accept small departures in the liberal side as well as in the conservative side, then the corrected resampled t-test appears to be a good choice. The advantage of the latter is that it requires little computing in comparison to the conservative $Z$ 

The paper revolved around a specific cross-validation estimator; one in which we split the data sets of n examples into a training set $\left( \mathrm { o f } \text{size} n _ { 1 } \right)$ and a testing set (of size $n _ { 2 } = n - n _ { 1 } )$ , and repeat this process $J$ times in an independent manner. $\mathrm { S o } .$ , for instance, the testing sets of two different splits may partially overlap. This contrasts with the most standard cross-validation estimator for which the testing sets are mutually exclusive. Analyzing the variance of this standard estimator and providing valid estimates of that variance would be valuable future work. 

## Appendix A: Some statistical prerequisites

Suppose that we observe data D that is generated by some probability mechanism $P ( D )$ Suppose that we are interested in some quantity $\mu = \mu ( P )$ and that we have derived an estimator $\hat { \mu }$ (based on $D )$ of the quantity of interest µ. Although the estimator $\hat { \mu }$ may have some nice properties such as being unbiased $( { \mathrm { i . e . ~ } } E [ { \hat { \mu } } ] = \mu )$ , the value $\hat { \mu }$ alone is not sufficient to say something interesting about $\mu$ . There are two questions that we might want to answer: (i) what are the plausible values of $\mu ? ,$ (ii) is a given value $\mu _ { 0 }$ plausible for $\mu ?$ Question (i) is answered with a confidence interval and question (ii) is resolved with a hypothesis test. 

Quite often $\hat { \mu }$ will be approximatively distributed as $N ( \mu , \operatorname{Var} [ \hat { \mu } ] )$ . If that is the case, for question (i) we consider the random interval $I = [ \hat { \mu } - z _ { 1 - \alpha / 2 } \sqrt { \operatorname{Var} [ \hat { \mu } ] } , \hat { \mu } + z _ { 1 - \alpha / 2 } \sqrt { \operatorname{Var} [ \hat { \mu } ] } ]$ with $z _ { 1 - \alpha / 2 }$ being the percentile $1 - \alpha / 2$ of the normal $N ( 0 , 1 )$ distribution, and called confidence interval $f o r \mu$ at confidence level $1 - \alpha$ . This random interval has the following property: $P ( \mu \in I ) \approx 1 - \alpha$ . For question (ii), if we want to assess if a hypothesis $H _ { 0 } { \mathrm { : } }$ $\mu = \mu _ { 0 }$ is plausible, we use the following criterion: reject $H _ { 0 } \operatorname { i f } | { \hat { \mu } } - \mu _ { 0 } | > z _ { 1 - \alpha / 2 } { \sqrt { \operatorname{Var} [ { \hat { \mu } } ] } }$ This is a test at the significance level α as Prob(reject $H _ { 0 } \mid \mathrm { H } _ { 0 }$ is true) ≈ $\alpha .$ 

However Var[µˆ ] is seldom known, it has to be estimated. If Var[ µˆ ] is a good estimator of Var[µˆ ], the above confidence interval and hypothesis test can be carried out with $\operatorname{Var} [ \hat { \mu } ]$ replaced by $\widehat { \operatorname{Var} } [ \hat { \mu } ]$ . Namely, the test of the hypothesis H<sub>0</sub>: $\mu = \mu _ { 0 } ( \mathrm { o f ~ s i z e } ^ { 1 5 } \alpha )$ has the following form 

$$
\text { reject } \quad H _ {0} \quad \text { if } | \hat {\mu} - \mu_ {0} | > z _ {1 - \alpha / 2} \sqrt {\widehat {\operatorname{Var}} [ \hat {\mu} ]},\tag{18}
$$

while the confidence interval for $\mu$ (at confidence level $1 - \alpha )$ will look like 

$$
\mu \in [ \hat {\mu} - z _ {1 - \alpha / 2} \sqrt {\widehat {\operatorname{Var}} [ \hat {\mu} ]}, \hat {\mu} + z _ {1 - \alpha / 2} \sqrt {\widehat {\operatorname{Var}} [ \hat {\mu} ]} ].\tag{19}
$$

When $\widehat { \operatorname{Var} } [ \hat { \mu } ]$ is used in lieu of $\operatorname{Var} [ \hat { \mu } ]$ (as done above), some people might prefer to replace $z _ { 1 - \alpha / 2 }$ by the percentile $1 - \alpha / 2$ of Student’s t distribution<sup>16</sup>; that is mostly motivated by the second result of Lemma 2. 

But what if $\widehat { \operatorname{Var} } [ \hat { \mu } ]$ is not a good estimator of Var[µˆ ]? We say that a confidence interval is liberal if it covers the quantity of interest with probability smaller than the required $1 - \alpha$ (Prob(µ $\in [ \widehat { \mu } - z _ { 1 - \alpha / 2 } \sqrt { \widehat { \operatorname{Var} } [ \widehat { \mu } ] } , \widehat { \mu } + z _ { 1 - \alpha / 2 } \sqrt { \widehat { \operatorname{Var} } [ \widehat { \mu } ] } ] ) < 1 - \alpha ) ;$ if the above probability is greater than $1 - \alpha ,$ , it is said to be conservative. A test is liberal if it rejects the null hypothesis with probability greater than the required size α whenever the null hypothesis is actually true $( P ( | \hat { \mu } - \mu _ { 0 } | > c \sqrt { \hat { \operatorname{Var} } [ \hat { \mu } ] } | \mu = \mu _ { 0 } ) > \alpha ~ ) ;$ if the above probability is smaller than $\alpha .$ , the test is said to be conservative. To determine if an inference procedure is liberal or conservative, we will ask ourself if $\widehat { \operatorname{Var} } [ \hat { \mu } ]$ tends to underestimate or overestimate Var[µˆ ]. Let us consider these two cases carefully. 

- If we have $\begin{array} { r } { \frac { \operatorname{Var} [ \hat { \mu } ] } { E [ \operatorname{Var} [ \hat { \mu } ] ] } > 1 } \end{array}$ , this means that $\widehat { \operatorname{Var} } [ \hat { \mu } ]$ ] tends to underestimate the actual variance of $\hat { \mu }$ so that the confidence interval of the form (19) will tend to be shorter than it needs to be to cover $\mu$ with probability $( 1 - \alpha )$ . So the confidence interval would cover the value $\mu$ with probability smaller than the required $( 1 - \alpha )$ , i.e. the interval would be liberal. In terms of hypothesis testing, the criterion shown in (18) will be met too often since $\widehat { \operatorname{Var} } [ \hat { \mu } ]$ tends to be smaller than it should. In other words, the probability of rejecting $H _ { 0 }$ when $H _ { 0 }$ is actually true will exceed the prescribed $\alpha .$ . We then say that the (actual) size of the test is greater than the nominal (or desired) size $\alpha$ 

- Naturally, the reverse happens $\begin{array} { r } { \mathrm { i f } \frac { \operatorname{Var} [ \hat { \mu } ] } { E [ \hat { \operatorname{Var} } [ \hat { \mu } ] ] } < 1 } \end{array}$ . So in this case, the confidence interval will tend to be larger than needed and thus will cover $\mu$ with probability greater than the required $( 1 - \alpha )$ , and the test of hypothesis based on the criterion (18) will tend to reject the null hypothesis with probability smaller than α (the nominal level of the test) whenever the null hypothesis is true. 

We shall call $\frac { \operatorname{Var} [ \hat { \mu } ] } { E [ \operatorname{Var} [ \hat { \mu } ] ] }$ the political ratio since it indicates that inference should be liberal when it is greater than 1, conservative when it is less than 1. Of course, the political ratio is not the only thing determining whether an inference procedure is liberal or conservative. For instance, if $\begin{array} { r } { \frac { \operatorname{Var} [ \hat { \mu } ] } { E [ \hat { \operatorname{Var} } [ \hat { \mu } ] ] } = 1 } \end{array}$ , the inference may still be liberal or conservative if the wrong <sup></sup>number of degrees of freedom is used, or if the distribution of $\hat { \mu }$ is not approximately Gaussian. 

In hypothesis testing, whether the size of the test is close to the nominal size $\alpha$ is not the only concern. We also want to know how the test behaves when the null hypothesis is false. Ideally, criterion (18) should often lead to rejection when the hypothesis is false and seldom reject $H_0$ when it is true. Define the power function as $\pi(\mu)=\operatorname{Prob}(\text{reject }H_0:\mu=\mu_0\mid\mu)$. This is the probability of rejection when the hypothesized value $\mu_0$ is held constant and the true value $\mu$ varies. We want the size of the test, $\operatorname{Prob}(\text{reject }H_0:\mu=\mu_0\mid H_0\text{ is true})=\pi(\mu_0)$, to be close to $\alpha$, and we want $\pi(\mu)$ to be large when $\mu\ne\mu_0$.

## A.1. Proof of Lemma 2

Let $W = ( W _ { 1 } , \dots , W _ { K } , W _ { K + 1 } ) \overset { i i d } { \sim } N ( 0 , \delta - \gamma )$ and $\epsilon \sim N ( \beta , \gamma )$ be $( K + 2 )$ independent Gaussian variates and let $U _ { k } = W _ { k } + \epsilon .$ , ∀k. One may easily show that $( U _ { 1 } , \dots , U _ { K + 1 } )$ follow the multivariate Gaussian distribution with the mean and covariance structure considered in Lemma 1. Let $\begin{array} { r } { \bar { W } = K ^ { - 1 } \sum _ { k = 1 } ^ { K } W _ { k } } \end{array}$ . Observe that 

$$
\bullet S _ {U} ^ {2} = \frac {1}{K - 1} \sum_ {k = 1} ^ {K} (U _ {k} - \bar {U}) ^ {2} = \frac {1}{K - 1} \sum_ {k = 1} ^ {K} (W _ {k} - \bar {W}) ^ {2} = S _ {W} ^ {2},
$$

$\bar { W }$ and $S _ { W } ^ { 2 }$ are independent with ${ \frac { ( K - 1 ) S _ { W } ^ { 2 } } { \delta - \gamma } } \sim \chi _ { K - 1 } ^ { 2 }$ (well known result), 

$S _ { W } ^ { 2 } , \bar { W } , \epsilon$ and $W _ { k + 1 }$ are four independent random variables. 

It then follows that 

$$
\begin{array}{l} \sqrt {1 - \pi} \frac {U _ {K + 1} - \beta}{\sqrt {S _ {U} ^ {2}}} \\ = \sqrt {\frac {\delta - \gamma}{\delta}} \frac {U _ {K + 1} - \beta}{\sqrt {S _ {U} ^ {2}}} = \frac {\frac {W _ {K + 1} + \epsilon - \beta}{\sqrt {\delta - \gamma + \gamma}}}{\sqrt {\frac {1}{K - 1} \frac {(K - 1) S _ {W} ^ {2}}{\delta - \gamma}}} = \frac {N (0 , 1)}{\sqrt {\frac {\chi_ {K - 1} ^ {2}}{K - 1}}} \sim t _ {K - 1}, \\ \sqrt {\frac {1 - \pi}{1 + (K - 1) \pi}} \frac {\sqrt {K} (\bar {U} - \beta)}{\sqrt {S _ {U} ^ {2}}} \\ = \frac {\sqrt {\delta - \gamma}}{\sqrt {\frac {\delta - \gamma}{K} + \gamma}} \frac {\bar {U} - \beta}{\sqrt {S _ {U} ^ {2}}} = \frac {\frac {\bar {W} + \epsilon - \beta}{\sqrt {\frac {\delta - \gamma}{K} + \gamma}}}{\sqrt {\frac {1}{K - 1} \frac {(K - 1) S _ {W} ^ {2}}{\delta - \gamma}}} = \frac {N (0 , 1)}{\sqrt {\frac {\chi_ {K - 1} ^ {2}}{K - 1}}} \sim t _ {K - 1}. \end{array}
$$

Recall that the $t _ { r }$ law is the distribution of $\frac { X } { { \sqrt { Y / r } } }$ where $X \sim N ( 0 , 1 )$ is independent of $Y \sim \chi _ { r } ^ { 2 }$ 

## A.2. Proof of Proposition 2

In order to show that $\sigma _ { 2 }$ is non-increasing in $n _ { 2 } .$ , it is sufficient to show that, for fixed $n _ { 1 }$ and arbitrary $n _ { 2 } > 1$ , we have σ $_ 2 ( n _ { 1 } , n _ { 2 } ) \leq \sigma _ { 2 } ( n _ { 1 } , n _ { 2 } - 1 )$ . 

We show later (we keep the fun part for the end) that 

$$
{ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { \infty } = \frac { 1 } { n } \sum _ { k = 1 } ^ { n } { } _ { n _ { 1 } } ^ { n _ { 2 } - 1 } \hat { \mu } _ { \infty } ^ { ( - k ) } ,\tag{20}
$$

where $^ { n _ { 2 } } _ { n _ { 1 } } \hat { \mu } _ { \infty }$ is as introduced after (8) and reproduced below, and $n _ { 2 } - 1 \hat { \mu } _ { \infty } ^ { ( - k ) }$ is the result of calculating $n _ { ^ 2 } - 1 \hat { \mu } _ { \infty }$ on $Z _ { 1 } ^ { n }$ with $Z _ { k }$ removed (leaving a data set of $n - 1 = n _ { 1 } + n _ { 2 } - 1$ examples). Obviously, the ${ } ^ { n _ { 2 } - 1 } \hat { \mu } _ { \infty } ^ { ( - k ) } \mathrm { { } ^ { s } }$ are identically distributed so that<sup>17</sup> 

$$
\sigma_ {2} (n _ {1}, n _ {2}) = \operatorname{Var} \bigl [ \begin{array}{c} n _ {2} \\ n _ {1} \end{array} \hat {\mu} _ {\infty} \bigr ] \leq \operatorname{Var} \bigl [ \begin{array}{c} n _ {2} - 1 \\ n _ {1} \end{array} \hat {\mu} _ {\infty} ^ {(- 1)} \bigr ] = \sigma_ {2} (n _ {1}, n _ {2} - 1).
$$

To complete the proof, we only need to show that identity (20) is true. 

Let $C ( S , n _ { 1 } )$ denote the set of all possible subsets of $n _ { 1 }$ distinct elements from $S ,$ , where $s$ is itself a set of distinct positive integers (of course $n _ { 1 }$ must not be greater than $\vert S \vert .$ the cardinality of S). For instance, the cardinality of $\begin{array} { r } { C ( S , n _ { 1 } ) \mathrm { i s } | C ( S , n _ { 1 } ) | = ( \binom { | S | } { n _ { 1 } } ) } \end{array}$ , i.e. the number of ways to choose $n _ { 1 }$ distinct elements from S. 

We have 

$$
\begin{array}{l} _ {n _ {1}} ^ {n _ {2}} \hat {\mu} _ {\infty} = \frac {1}{\binom {n} {n _ {1}}} \sum_ {s \in C (\{1, \dots , n \}, n _ {1})} \frac {1}{n _ {2}} \sum_ {i \in \{1, \dots , n \} \setminus s} \mathcal {L} (Z _ {s}; Z _ {i}) \\ = \frac {1}{\binom {n} {n _ {1}}} \sum_ {s \in C (\{1, \dots , n \}, n _ {1})} \frac {1}{n _ {2} (n _ {2} - 1)} \sum_ {k \in \{1, \dots , n \} \setminus s} \sum_ {i \in (\{1, \dots , n \} \setminus s) \setminus \{k \}} \mathcal {L} (Z _ {s}; Z _ {i}) \\ = \frac {n _ {1} ! n _ {2} !}{n ! n _ {2}} \sum_ {k = 1} ^ {n} \sum_ {s \in C (\{1, \dots , n \} \setminus \{k \}, n _ {1})} \frac {1}{n _ {2} - 1} \sum_ {i \in (\{1, \dots , n \} \setminus \{k \}) \setminus s} \mathcal {L} (Z _ {s}; Z _ {i}) \\ = \frac {1}{n} \sum_ {k = 1} ^ {n} \frac {1}{\binom {n - 1} {n _ {1}}} \sum_ {s \in C (\{1, \dots , n \} \setminus \{k \}, n _ {1})} \frac {1}{n _ {2} - 1} \sum_ {i \in (\{1, \dots , n \} \setminus \{k \}) \setminus s} \mathcal {L} (Z _ {s}; Z _ {i}) \\ = \frac {1}{{n}} \sum_ {k = 1} ^ {{n}} ^ {{n _ {2}} - 1} _ {{n _ {1}}} {\hat {\mu}} _ {\infty} ^ {{(- k)}}. \end{array}
$$

Note that to get from the first to second line in the above development, we used the following identity for the arithmetic mean (of $\begin{array} { r } { x _ { 1 } , \dots x _ { I } \mathrm { ~ s a y } ) : \frac { 1 } { I } \sum _ { i = 1 } ^ { I } \bar { x _ { i } } = \frac { 1 } { I ( I - 1 ) } \sum _ { k = 1 } ^ { I } \sum _ { i \ne k } x _ { i } } \end{array}$ 

## A.3. Inference when vectors have moments as in Lemma 1

Suppose that we have n independent and identically distributed random vectors $T _ { 1 } , \ldots , T _ { i } , \ldots , T _ { n }$ where $T _ { i } = ( T _ { i , 1 } , \ldots , T _ { i , K } ) ^ { \prime }$ . Suppose that $T _ { i , 1 } , \ldots , T _ { i , K }$ has the moment structure displayed in Lemma 1. Let $\begin{array} { r } { \bar { T } _ { i } = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } T _ { i , k } } \end{array}$ . Let $\theta = ( \beta , \delta , \pi )$ be the vector of parameters involved in Lemma 1. Consider the following unbiased estimating function 

$$
g (\theta) = \sum_ {i = 1} ^ {n} g _ {i} (\theta) = \sum_ {i = 1} ^ {n} \left( \begin{array}{c} \bar {T} _ {i} - \beta \\ \sum_ {k = 1} ^ {K} [ (T _ {i, k} - \beta) ^ {2} - \delta ] \\ (\bar {T} _ {i} - \beta) ^ {2} - \delta \left(\pi + \frac {1 - \pi}{K}\right) \end{array} \right).
$$

Let $\begin{array} { r } { B ( \theta ) = \sum _ { i = 1 } ^ { n } g _ { i } ( \theta ) g _ { i } ( \theta ) ^ { \prime } } \end{array}$ and 

$$
A (\theta) = - E \left[ \frac {\partial g (\theta)}{\partial \theta^ {\prime}} \right] = n \left[ \begin{array}{c c c} 1 & 0 & 0 \\ 0 & K & 0 \\ 0 & \left(\pi + \frac {1 - \pi}{K}\right) & \frac {K - 1}{K} \delta \end{array} \right].
$$

Let $\hat { \theta }$ be such that $g ( \hat { \theta } ) = \mathbf { 0 } _ { 3 }$ , then, according to White (1982), 

$$
\theta_j \in \left[\hat{\theta}_j - z_{1-\alpha/2}\sqrt{\hat{V}[\hat{\theta}_j]},\ \hat{\theta}_j + z_{1-\alpha/2}\sqrt{\hat{V}[\hat{\theta}_j]}\right],
$$

with $\hat { V } [ \hat { \theta } _ { j } ] = [ A ( \hat { \theta } ) ^ { - 1 } B ( \hat { \theta } ) ( A ( \hat { \theta } ) ^ { - 1 } ) ^ { \prime } ] _ { j , j } .$ , is a confidence interval at approximate confidence level $( 1 - \alpha )$ . For instance, in the case of $\beta _ { ; }$ , this yields 

$$
\beta = \theta_ {1} \in \left[ \bar {T}. \pm Z _ {1 - \alpha / 2} \sqrt {\frac {1}{n} \frac {1}{n} \sum_ {i = 1} ^ {n} (\bar {T} _ {i} - \bar {T}) ^ {2}} \right],
$$

where $\begin{array} { r } { \bar { T } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \bar { T } _ { i } } \end{array}$ is the mean of all the ${ { \bar { T } } _ { i } } ^ { \mathrm { ~ , ~ } } \mathrm { ~ }$ s. 

## Notes



1. Here we are not trying to prove the conjecture but to justify our intuition that it is correct. 



2. When n is odd, everything is the same except that splitting the data in two will result in a leftover observation that is ignored. Thus $D _ { m }$ and $D _ { m } ^ { c }$ are still disjoint subsets of size $\lfloor { \frac { n } { 2 } } \rfloor$ from $Z _ { 1 } ^ { n }$ , but $Z _ { 1 } ^ { n } \backslash ( D _ { m } \cup D _ { m } ^ { c } )$ is a singleton instead of being the empty set. 

3. Independence holds if the train/test subsets selection process in $D _ { 1 }$ is independent of the process in $D _ { 1 } ^ { c } .$ . Otherwise, $\hat { \mu } _ { 1 }$ and $\hat { \mu } _ { 1 } ^ { c }$ may not be independent, but they are uncorrelated, which is all we actually need. 

4. At this point, we encourage readers to consult Appendix A. 

5. We note that this statistic is closely related to the McNemar statistic (Everitt, 1977) when the problem at hand is the comparison of two classification algorithms, i.e. L is of the form (4) with Q of the form $( 2 ) .$ Indeed, let $L _ { A - B } ( 1 , i ) = L _ { A } ( 1 , i ) - L _ { B } ( 1 , i )$ where $L _ { A } ( 1 , i )$ indicates whether $Z _ { i }$ is misclassified $( L _ { A } ( 1 , i ) = 1 )$ by algorithm A or not $( L _ { A } ( 1 , i ) = 0 ) ; L _ { B } ( 1 , i )$ is defined likewise. Of course, algorithms A and B share the same training set $( S _ { 1 } )$ and testing set (S<sup>c</sup>). We have $\begin{array} { r } { n _ { 1 } \hat { \mu } _ { 1 } = \frac { n _ { 1 0 } - n _ { 0 1 } } { n _ { 2 } } } \end{array}$ , with $n _ { j k }$ being the number of times $L _ { A } ( 1 , i ) = j$ and $L _ { B } ( 1 , i ) = k , j = 0 , 1 , k = 0 , 1$ . McNemar’s statistic is devised for testing $H _ { 0 } \colon \ J _ { n _ { 1 } } \mu = 0 ( \mathrm { i . e }$ . the $L _ { A - B } ( 1 , i ) \mathrm { ^ s }$ have expectation 0) so that one may estimate the variance of the $L _ { A - B } ( 1 , i ) \mathrm { ^ s }$ with the mean of the $( L _ { A - B } ( 1 , i ) - 0 ) ^ { 2 } \mathrm { { ^ s } }$ s (which is $\textstyle { \frac { n _ { 0 1 } + n _ { 1 0 } } { n _ { 2 } } } $ rather than with $S _ { L } ^ { 2 }$ . Then (12) becomes 

$$
\text { reject } H _ {0} \text { if } \left| \frac {n _ {1 0} - n _ {0 1}}{\sqrt {n _ {1 0} + n _ {0 1}}} \right| > z _ {1 - \alpha / 2},
$$

with $z _ { p }$ the quantile $p$ of N (0, 1), which squared leads to the McNemar’s test (not corrected for continuity). 6. From this, we can rederive that $S _ { L } ^ { 2 }$ is biased for the unconditional variance as follows: 

$$
\begin{array}{l} E \big [ S _ {L} ^ {2} \big ] = E \big [ E \big [ S _ {L} ^ {2} \big | Z _ {S _ {1}} \big ] \big ] = E \big [ \mathrm{Var} \big [ L (1, i) \big | Z _ {S _ {1}} \big ] \big ] \\ \leq E \big [ \mathrm{Var} \big [ L (1, i) \big | Z _ {S _ {1}} \big ] \big ] + \mathrm{Var} \big [ E \big [ L (1, i) \big | Z _ {S _ {1}} \big ] \big ] = \mathrm{Var} [ L (1, i) ]. \end{array}
$$

7. When the problem at hand is the comparison of two classification algorithms, i.e., L is of the form (4) with Q of the form (2), this approach is what Dietterich (1998) calls the “resampled paired t-test” statistic. 

8. Dietterich only considered the comparison of two classification algorithms, that is L of the form (4) with Q of the form (2). 

9. The parameters of the simulations displayed in Tables 2–4 were more or less chosen arbitrarily. However, efforts were made so that one or two simulations for each problem would correspond to ${ } _ { n _ { 1 } } \mu _ { A - B } = 0 \mathrm { ( i . e }$ • , ${ } _ { n _ { 1 } } \mu _ { A } = { } _ { n _ { 1 } } \mu _ { B } )$ 

10. The function tree in Splus 4.5 for Windows with default options and no pruning was used to train the regression tree. 

11. $\hat { \beta } _ { Z _ { S } }$ includes an intercept and correspondingly 1 was included in the input vector X. 

12. We used the function tree in Splus version 4.5 for Windows. The default arguments were used and no pruning was performed. The function predict with option $t y p e = \ " { c l a s s } ^ { * }$ was used to retrieve the decision function of the tree. 

13. As mentioned before, the corrected pseudo-bootstrap and the corrected resampled t-test are typically used in cases where training sets are 5 or 10 times larger than test sets. So we must only be concerned with $\rho ( \frac { n } { 2 }$ , <sup>n</sup> ) and ρ $( { \frac { 9 n } { 1 0 } } , { \frac { n } { 1 0 } } )$ 

14. Actually in figure 2 we do see that the corrected resampled t-test with $\begin{array} { r } { n _ { 2 } = \frac { n } { 1 0 } } \end{array}$ is liberal in Simulations 2 and 4 despite the fact tha $\rho _ { A - B } ( \textstyle { \frac { n } { 2 } } , \textstyle { \frac { n } { 1 0 } } )$ do not differ significantly from $\scriptstyle { \frac { 1 } { 6 } }$ in Simulation 2 and $\rho _ { A - B } ( { \frac { n } { 2 } } , { \frac { n } { 1 0 } } )$ is barely significantly smaller than $\frac { 1 } { 6 }$ in Simulation 4. But, as mentioned in Appendix A, the political ratio Var[µˆ ] is not the only thing determining whether inference is liberal or conservative. What happens in this E[σˆ <sup>2</sup>] particular case is that the distribution of $\mathbf { \bar { \rho } } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { 1 5 }$ is asymmetric; ${ } _ { n _ { 1 } } ^ { n _ { 2 } } \hat { \mu } _ { 1 }$ did not appear to suffer from this problem. The comparison of algorithm A and B for the regression problem is the only place where this phenomenon was substantial in our simulation. That is why curves (other than t-test and Dietterich’ $; 5 \times 2$ cv that are based on ${ } _ { n _ { 1 } \hat { \mu } _ { 1 } ) } ^ { n _ { 2 } }$ are asymmetric and bottom out before the actual value of $n / 2 \mu _ { A - B }$ (laying between the vertical dotted lines). We don’t observe this in other figures. 

15. Size is a synonym of significance level. 

16. The Student’s distribution with k degrees of freedom refers to the law of $\frac { Z } { \sqrt { Y / k } }$ where $Z \sim N ( 0$ , 1) is independent of $Y \sim \chi _ { k } ^ { 2 }$ . Often, the $\bar { Y }$ random variable will take the form $\textstyle Y ^ { \vee } = \sum _ { i = 1 } ^ { N } R _ { i } ^ { 2 }$ . This will have $( N - p )$ degrees of freedom where p is the number of linear constraints the $R _ { i } { } ^ { \ ' } \mathrm { s }$ are subject to. For instance, if $R _ { i } = X _ { i } - \bar { X }$ , then $\begin{array} { r } { p = 1 \mathrm { { a s } } \sum _ { i = 1 } ^ { N } R _ { i } = 0 . } \end{array}$ 

17. Let $U _ { 1 } , \dots , U _ { n }$ be variates with equal variance and let $\begin{array} { r } { \bar { U } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } U _ { i } } \end{array}$ , then we have Var $[ \bar { U } ] \leq \operatorname{Var} [ U _ { 1 } ]$ 

## References



Blake, C., Keogh, E., & Merz, C.-J. (1998). UCI repository of machine learning databases. 





Breiman, L. (1996). Heuristics of instability and stabilization in model selection. Annals of Statistics, 24:6, 2350– 2383. 





Breiman, L., Friedman, J., Olshen, R., & Stone, C. (1984). Classification and regression trees. Wadsworth International Group. 





Burges, C. (1998). A tutorial on support vector machines for pattern recognition. Data Mining and Knowledge Discovery, 2:2, 1–47. 





Devroye, L., Györfi, L., & Lugosi, G. (1996). A probabilistic theory of pattern recognition. Springer-Verlag. 





Dietterich, T. (1998). Approximate statistical tests for comparing supervised classification learning algorithms. Neural Computation, 10:7, 1895–1924. 





Efron, B., & Tibshirani, R. J. (1993). An introduction to the bootstrap. Monographs on Statistics and Applied Probability 57. New York, NY: Chapman & Hall. 





Everitt, B. (1977). The analysis of contingency tables. London: Chapman & Hall. 





Goutte, C. (1997). Note on free lunches and cross-validation. Neural Computation, 9:6, 1053–1059. 





Hinton, G., Neal, R., Tibshirani, R., & DELVE team members. (1995). Assessing learning procedures using DELVE. Technical report, University of Toronto, Department of Computer Science. 





Kearns, M., & Ron, D. (1997). Algorithmic stability and sanity-check bounds for leave-one-out cross-validation. Tenth Annual Conference on Computational Learning Theory (pp. 152–162). Morgan Kaufmann. 





Kohavi, R. (1995). A study of cross-validation and bootstrap for accuracy estimation and model selection. Proceeding of the Fourteenth International Joint Conference on Artificial Intelligence (pp. 1137–1143). Morgan Kaufmann. 





Kolen, J. & Pollack, J. (1991). Back propagation is sensitive to initial conditions. Advances in Neural Information Processing Systems (pp. 860–867). San Francisco, CA: Morgan Kauffmann. 





Nadeau, C., & Bengio, Y. (1999). Inference for the generalisation error. Technical report 99s-25, CIRANO. 





Vapnik, V. (1982). Estimation of dependences based on empirical data. Berlin: Springer-Verlag. 





White, H. (1982). Maximum likelihood estimation of misspecified models. Econometrica, 50, 1–25. 





Wolpert, D., & Macready, W. (1995). No free lunch theorems for search. Technical report SFI-TR-95-02-010, The Santa Fe Institute. 





Zhu, H., & Rohwer, R. (1996). No free lunch for cross validation. Neural Computation, 8:7, 1421–1426. 





Received August 16, 1999 





Revised June 21, 2001 





Accepted June 21, 2001 





Final manuscript February 7, 2002 

