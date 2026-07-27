# EQUIVALENT COMPARISONS OF EXPERIMENTS[^1]

By David Blackwell 

Stanford University and Howard University 

Received 11/17/52.

[^1]: This paper was prepared under an Office of Naval Research Contract.

> **Editorial note.** This Markdown edition normalizes notation and repairs formulas or omitted steps when required by the internal mathematical logic of the argument. It is not a diplomatic transcription of the printed source.

## 1. Summary

Sherman [8] and Stein [9] have shown that a method given by the author [1] for comparing two experiments is equivalent, for experiments with a finite number of outcomes, to the original method introduced by Bohnenblust, Shapley, and Sherman [4]. A new proof of this result is given, and the restriction to experiments with a finite number of outcomes is removed. A class of weaker comparisons—comparison in k-decision problems—is introduced, in three equivalent forms. For dichotomies, all methods are equivalent, and can be described in terms of errors of the first and second kinds. 

## 2. Introduction

An ordered collection $\alpha = (m_{1}, \cdots, m_{n})$ of probability measures on a Borel field $\mathfrak{B}$ of subsets of a space $X$ will be called an experiment. Any pair $(\alpha, A)$, where $A$ is a closed bounded convex subset of n-space, corresponds to a decision problem as follows. A point $x \in X$ is selected according to one of the distributions $m_{i}$; the statistician observes $x$ and then chooses an action $d$ from a given set $D$, incurring a loss $L(i, d)$. If we associate with $d$ the vector $w(d) = (L(1, d), \cdots, L(n, d))$, the range of $w(d)$ as $d$ varies over $D$ is the set $A$ associated with the problem. Thus we may replace $D$ by $A$, and suppose that the statistician chooses a point $a = (a_{1}, \cdots, a_{n}) \in A$, incurring loss $a_{i}$ when $m_{i}$ is the distribution of $x$. By using randomized decision procedures we increase $A$ to its convex hull, and for simplicity we suppose $A$ closed and bounded as well as convex. 

A decision function in the problem $(\alpha, A)$ is a $\mathfrak{B}$-measurable function $f$ from $X$ into $A$, specifying for each $x$ the action $a = f(x)$ to be taken when $x$ is observed. When $m_{i}$ is the distribution of $x$, the expected loss from $f$ is $v_{i}(f) = \int a_{i}(x)\,dm_{i}(x)$; the vector $v(f) = (v_{1}(f), \cdots, v_{n}(f))$ is called the loss vector of $f$, and the range of $v(f)$ as $f$ varies over all decision functions in the problem $(\alpha, A)$ will be denoted by $B(\alpha, A)$. The set $B(\alpha, A)$ will be a closed, bounded, convex subset of n-space [2]. 

For two experiments $\alpha$, $\beta$ with the same $n$, following Bohnenblust, Shapley, and Sherman, we say that $\alpha$ is more informative than $\beta$, written $\alpha \supset \beta$, if for every $A$ we have $B(\alpha, A) \supset B(\beta, A)$, that is if every loss vector attainable in problem $(\beta, A)$ is also attainable in $(\alpha, A)$. For any experiment $\alpha = (m_{1}, \cdots, m_{n})$, let $p_{i}(x)$ be the density of $m_{i}$ with respect to $\sum_{i=1}^{n} m_{i}$, let $p(x) = [p_{1}(x), \cdots, p_{n}(x)]$, and let $m_{\alpha}$ denote the distribution of $p(x)$ when $x$ has distribution $\sum_{i=1}^{n} m_{i}/n$. Then $m_{\alpha}$ is a probability measure defined on the set $P$ of all vectors $p = (p_{1}, \dots, p_{n})$ with $p_i \geq 0$ and $\sum_{i=1}^{n} p_i = 1$, and 

$$
\int p_i\,dm_{\alpha} = 1/n. \tag{1}
$$

the center of gravity of $m_{\alpha}$ is the point $(1/n, \cdots, 1/n)$ . The measure $m_{\alpha}$ is called by Bohnenblust, Shapley, and Sherman the standard measure associated with the experiment $\alpha$ . Their basic results connecting $m_{\alpha}$ and $\supset$ are summarized as Theorem 1 below (for a proof see [1]). 

**THEOREM 1.** Every probability measure on $P$ with property (1) is the standard measure of some experiment; two experiments $\alpha$ and $\beta$ have the same standard measure if and only if $B(\alpha, A) = B(\beta, A)$ for all $A$; $\alpha \supset \beta$ if and only if for every continuous convex function $\phi(p)$ on $P$, $\int \phi\,dm_{\alpha} \geq \int \phi\,dm_{\beta}$. 

An alternative method of comparing two experiments $\alpha, \beta$, introduced by the author [1], can best be described in terms of the concept of stochastic transformation. If $\mathfrak{B}$, $\mathfrak{C}$ are Borel fields of subsets of $X$, $Y$ respectively, a stochastic transformation $T$ is a function $Q(x, E)$ defined for all $x \in X$ and $E \in \mathfrak{C}$ which for fixed $E$ is a $\mathfrak{B}$-measurable function of $x$ and for fixed $x$ is a probability measure on $\mathfrak{C}$. For any probability measure $m$ on $\mathfrak{B}$, the function $M(E) = \int Q(x, E)\,dm(x)$ is a probability measure on $\mathfrak{C}$, denoted by $Tm$. If $X, Y$ are Borel sets in n-space and $\mathfrak{B}$, $\mathfrak{C}$ are the Borel subsets of $X, Y$, $T$ is called mean-preserving if $\int y\,dQ(x, y) = x$ for all $x$. 

If $\alpha = (m_{1}, \cdots, m_{n})$ and $\beta = (M_{1}, \cdots, M_{n})$ are two experiments, with $m_{i}$, $M_{i}$ defined on Borel fields $\mathfrak{B}$, $\mathfrak{C}$ of $X$, $Y$ respectively, we shall say that $\alpha$ is sufficient for $\beta$, written $\alpha \succ \beta$, if there is a stochastic transformation $T$ with $Tm_{i} = M_{i}$ for $i = 1, \cdots, n$. Thus $\alpha \succ \beta$ means that the statistician, observing the result $x$ of $\alpha$, can, by selecting $y$ according to $Q(x, E)$, obtain a result equivalent to the result of observing $\beta$. 

The concept $\succ$ also has a description in terms of standard measures, summarized in 

**THEOREM 2.** [1]. $\alpha \succ \beta$ if and only if there is a mean-preserving stochastic transformation $T$ with $Tm_{\beta} = m_{\alpha}$. 

If $\alpha \succ \beta$ and $\phi$ is any continuous convex function on $P$, 

$$
\begin{aligned}
\int \phi\,dm_{\alpha}
&= \int \left(\int \phi(p)\,dQ(q,p)\right)dm_{\beta}(q) \\
&\geq \int \phi\left(\int p\,dQ(q,p)\right)dm_{\beta}(q) \\
&= \int \phi\,dm_{\beta},
\end{aligned}
$$

so that, from Theorem 1 we obtain 

**THEOREM 3.** $\alpha \succ \beta$ implies $\alpha \supset \beta$. 

The converse of Theorem 3 has been proved, for experiments with a finite number of outcomes, by Sherman [8] and Stein [9]. In Section 3 we give a new proof of the Sherman-Stein theorem, and in Section 4 extend the theorem to arbitrary experiments. 

## 3. The Sherman-Stein Theorem

If the space $X$ of outcomes of the experiment $\alpha$ is finite, consisting say of $x_{1}, \cdots, x_{N}$, then $\alpha$ is characterized by the $n \times N$ Markov matrix $P = \lVert p_{ij} \rVert$, where $p_{ij} = m_{i}(x_{j})$, and conversely every Markov matrix can be interpreted as an experiment. For two Markov matrices $P$, $Q$ with the same $n$, we write $P \supset Q$, $P \succ Q$ if the corresponding experiments are related by $\supset$, $\succ$ respectively. 

**THEOREM 4.** If $P, Q$ are $n \times N_1$, $n \times N_2$ Markov matrices with $P \supset Q$, then for every $N_2 \times n$ matrix $D$ there is an $N_1 \times N_2$ Markov matrix $M$ with 

$$
\operatorname{Trace}(PMD) \leq \operatorname{Trace}(QD).
$$

**PROOF.** Let $A$ be the convex hull of the rows of $D$. The decision function $f$ in problem $(Q, A)$ selecting the $j$th row of $D$ when $j$ is observed has $v_{i}(f) = \sum_{j} q_{ij} d_{ji}$, the $i$th diagonal element of $QD$. 

Since $P \supset Q$ , there is a decision function $g$ in problem $(P, A)$ , selecting say $a_j \in A$ when $j$ is observed, with $v_i(g) = \sum_j p_{ij} a_{ji} = v_i(f)$ for all $i$ . Since $a_j \in A$ , there are nonnegative numbers $m_{jk}$ with $\sum_k m_{jk} = 1$ such that $a_{ji} = \sum_k m_{jk} d_{ki}$ for all $i$ . Thus $v_i(g) = \sum_{j,k} p_{ij} m_{jk} d_{ki}$ , which is the $i$ th diagonal element of $PMD$ . It follows that $M$ has not only the property asserted in the theorem but the stronger property that $PMD$ and $QD$ have identical diagonal elements. 

**THEOREM 5.** $P \succ Q$ if and only if there is a Markov matrix $M$ with $PM = Q$. 

This is simply a restatement of the definition of $\succ$ for the special case $X = (1, \cdots, N_{1})$ , $Y = (1, \cdots, N_{2})$ , since a stochastic transformation becomes simply an $N_{1} \times N_{2}$ Markov matrix. 

**THEOREM 6 (Sherman-Stein theorem).** $P \supset Q$ implies $P \succ Q$. 

**PROOF.** Consider the function $h(D, M) = \operatorname{Trace}((Q - PM)D)$, as $M$ varies over all $N_1 \times N_2$ Markov matrices and $D$ varies over all $N_2 \times n$ matrices with $0 \leq d_{ki} \leq 1$ for all $k, i$. Since $h$ is bilinear and the ranges of $D, M$ are closed, bounded, and convex, $h$ has a saddle point [3], that is, there exist $D_0, M_0$ with $h(D_0, M) \geq h(D_0, M_0) \geq h(D, M_0)$ for all $D, M$. The proof of Theorem 4 established the stronger fact that, for every $D$, one can choose $M$ such that $PMD$ and $QD$ have identical diagonal elements. In particular, for $D_0$ there is an $M$ with $h(D_0,M)=0$. Consequently $h(D,M_0)\leq 0$ for every $D$. Writing $U = Q - PM_0$, we have 

$$
\operatorname{Trace}(UD) \leq 0 \quad \text{for all } D,
$$

so that $u_{ik} \leq 0$ for all $i, k$. Since $U$ is the difference of two Markov matrices, $\sum_{i,k} u_{ik} = 0$, so that $u_{ik} = 0$ for all $i, k$ and $PM_0 = Q$. Thus by Theorem 5, $P \succ Q$. 

An alternative form of the Sherman-Stein theorem is 

**THEOREM 7.** If $m_1$ and $m_2$ are any two probability measures on a finite subset $X$ of n-space such that for every continuous convex $\phi$ defined on the convex hull of $X$, $\int \phi\,dm_1 \geq \int \phi\,dm_2$, then there is a mean-preserving stochastic transformation $T$ with $Tm_2 = m_1$. 

From Theorems 1 and 2, Theorem 7 implies Theorem 6. Theorem 7 was proved for n = 1 by Hardy, Littlewood, and Polya [6], for n = 2 without the restriction that X be finite by the author, and in the form given here by Sherman [8] and Stein [9]. 

**PROOF OF THEOREM 7.** From Theorems 1 and 2, Theorem 6 implies Theorem 7 if $X \subset P$ and the common center of gravity of $m_{1}$, $m_{2}$ is $(1/n, \cdots, 1/n)$, since in this case $m_{1}$, $m_{2}$ are the standard measures of experiments. Imbedding $X$ in $n + 1$ space and performing an appropriate linear transformation reduces the general case in n-space to that of standard measures in $n + 1$ space and completes the proof. 

A direct proof of Theorem 7, using the methods of Theorem 6 and not appealing to Theorems 1 and 2 can be given. 

## 4. Equivalence of $\supset$ and $\succ$

In this section we extend Theorem 7, replacing the requirement that $X$ be finite by the weaker requirement that $X$ be bounded. For any two probability measures $m$, $M$ on a bounded subset $X$ of n-space, we write $M \supset m$ if for every continuous convex $\phi$ on the convex hull of $X$, $\int \phi\,dM \geq \int \phi\,dm$, and $M \succ m$ if there is a mean-preserving stochastic transformation (abbreviated m.p.s.t.) $T$ with $Tm = M$. We shall prove 

**THEOREM 8.** If $M \supset m$, then $M \succ m$. 

The method of proof consists of approximating $m$ , $M$ by measures concentrated on finite sets and using Doob's martingale convergence theorems. We first prove 

**A.** There exist sequences of measures $m_N$, $M_N$, each concentrated on a finite set, with
$m_N \prec m_{N+1} \subset m \subset M \prec M_{N+1} \prec M_N$ for all $N$, such that

$$
m_N \Rightarrow m,
\qquad
M_N \Rightarrow M
\quad \text{as } N \rightarrow \infty, \tag{2}
$$

Here $\Rightarrow$ denotes weak convergence; equivalently, the integrals of every bounded continuous function converge.

**PROOF.** For any n-vector $a = (a_{1}, \cdots, a_{n})$ with integral coordinates, let $C(N, a)$ denote the cube consisting of all $t = (t_{1}, \cdots, t_{n})$ with $2^{-N}a_{i} \leq t_{i} < 2^{-N}(a_{i} + 1)$. Let $Z(N, a)$ be the center of gravity of $m$ on $C(N, a)$ whenever $m(C(N,a))>0$, and let $m_{N}$ assign to $Z(N, a)$ measure $m(C(N, a))$. Cells of zero $m$-measure may be ignored. The diameter of the cells tends to zero, so $m_N \Rightarrow m$. Because the partitions are nested, the conditional-barycenter construction gives $m_N \prec m_{N+1}$; Jensen's inequality gives $m_{N+1} \subset m$. 

To define $M_{N}$, let $Q_{N}(t, E)$ for $t \in C(N, a)$ concentrate on the $2^{n}$ vertices of $C(N, a)$. At the vertex

$$
2^{-N}(a_{1} + \epsilon_{1}, \cdots, a_{n} + \epsilon_{n}),
\qquad \epsilon_i \in \{0,1\},
$$

assign mass $\prod_{i=1}^n b_i$, where

$$
b_i =
\begin{cases}
a_i + 1 - 2^N t_i, & \epsilon_i = 0,\\
2^N t_i - a_i, & \epsilon_i = 1.
\end{cases} \tag{3}
$$

For each $i$, the two possible values of $b_i$ are nonnegative and sum to one. Hence the masses of all $2^n$ vertices sum to one. Their barycenter is $t$, so $Q_N$ is a mean-preserving stochastic transformation $U_N$. Define $M_N=U_NM$. The distance from $t$ to every selected vertex is at most $\sqrt n\,2^{-N}$, which implies $M_N\Rightarrow M$. Moreover, $M_N=U_NM_{N+1}$, so $M_N$ has the required order properties.

**B.** There exist sequences $T_N, V_N, W_N$ of m.p.s.t. each from a finite set of n-space to a finite set of n-space with 

$$
\text { (a) } \quad m _ {N + 1} = T _ {N} m _ {N}, \quad \text {(b)} \quad M _ {N - 1} = V _ {N} M _ {N}, \quad \text {(c)} \quad M _ {N} = W _ {N} m _ {N},
$$

and 

$$
(\mathrm{d}) \quad W _ {N} = V _ {N + 1} W _ {N + 1} T _ {N}.
$$

**PROOF.** From A there exist sequences $T_{N}$ and $V_{N}$ with properties (a) and (b). Also from A, $m_{N} \subset M_{N}$, so that, from Theorem 7, there is a m.p.s.t. $Y_{N}$ from a finite set to a finite set with $M_{N} = Y_{N}m_{N}$. For $D > N$, write 

$$
Y _ {N D} = V _ {N + 1} \dots V _ {D} Y _ {D} T _ {D - 1} \dots T _ {N},
$$

so that 

$$
Y _ {N D} = V _ {N + 1} Y _ {N + 1, D} T _ {N}
$$

$$
\text { for } D > N + 1,
$$

and 

$$
M _ {N} = Y _ {N D} m _ {N}
$$

$$
\text { for } D > N.
$$

Let $D \to \infty$ through a subsequence for which $Y_{ND}$ converges for all $N$ , say to $W_N$ . Then $W_N$ satisfies (c) and (d). 

**PROOF OF THEOREM 8.** We specify the joint distribution of two sequences $x_{1}, x_{2}, \cdots$, $y_{1}, y_{2}, \cdots$ of n-dimensional chance variables by 

**C.** For any $N$, the variables $x_{1}, \cdots, x_{N}, y_{N}, \cdots, y_{1}$ form a Markov chain in the order written. The distribution of $x_{1}$ is $m_{1}$ and the conditional distributions of $x_{i+1}$ given $x_{i}$, $y_{N}$ given $x_{N}$, and $y_{i-1}$ given $y_{i}$, are specified by $T_{i}$, $W_{N}$, and $V_{i}$ respectively. 

Part (d) of B guarantees that the requirements C are consistent, and Kolmogorov's extension theorem [7] then asserts the existence of $x_{1}, x_{2}, \cdots, y_{1}, y_{2}, \cdots$ , with property C. Parts (a), (b), (c) of B imply that $x_{N}, y_{N}$ have distributions $m_{N}, M_{N}$ respectively. Also the sequence 

$$
x _ {1}, x _ {2}, \dots , \dots , y _ {2}, y _ {1}
$$

forms a martingale [5] in the order written; by Doob's martingale theorem [5], $x_{N} \to x^{*}$, $y_{N} \to y^{*}$ as $N \to \infty$, and $E(y^{*} \mid x^{*}) = x^{*}$. From A, $x^{*}$ and $y^{*}$ have distributions $m$, $M$ respectively, so that $Q(x, E) = \operatorname{Prob}\{y^{*} \in E \mid x^{*} = x\}$ is a m.p.s.t. $T$ with $Tm = M$. This completes the proof. 

## 5. k-decision problems

In this section we introduce a comparison somewhat weaker than $\succ$. The following lemma will be useful. 

**LEMMA.** For any experiment $\alpha$ and any closed, bounded set $C$ with convex hull $A$, $B(\alpha, A)$ is the convex hull of $B(\alpha, C)$. 

**PROOF.** Since both $B(\alpha, A)$ and $B(\alpha, C)$ are closed and $B(\alpha, A)$ is convex [2], it suffices to show that every $v(f) \in B(\alpha, A)$ can be approximated by points in the convex hull of $B(\alpha, C)$. We may suppose that $f$ assumes only a finite number of values $a_{1}, \cdots, a_{N}$, since every $f$ can be approximated by $f$'s of this kind. Say 

$$
S_j = \{x:f(x) = a_j\}, \qquad
a_j = \sum_{i=1}^{r} \lambda_{ji}c_i, \qquad
\lambda_{ji} \geq 0, \qquad
\sum_i \lambda_{ji} = 1.
$$

For any multi-index $h=(h_1,\ldots,h_N)\in\{1,\ldots,r\}^N$, define the decision function $f_h$ and its weight $\lambda(h)$ by

$$
f_h(x) = c_{h_j} \quad \text{for } x \in S_j,
\qquad
\lambda(h) = \prod_{j=1}^{N} \lambda_{j h_j}.
$$

Since $\sum_h\lambda(h)=\prod_{j=1}^N\sum_{i=1}^r\lambda_{ji}=1$, the expression $\sum_h\lambda(h)v(f_h)$ is a convex combination of points in $B(\alpha,C)$. Its $s$th coordinate is

$$
\begin{aligned}
\sum_h \lambda(h)\sum_j \int_{S_j} c_{h_j s}\,dm_s
&= \sum_{h,j} m_s(S_j)\bigl(c_{h_j s}\lambda(h)\bigr) \\
&= \sum_j m_s(S_j)
   \left(\sum_i c_{is}
   \left(\sum_{h:\,h_j=i}\lambda(h)\right)\right) \\
&= \sum_j m_s(S_j)\left(\sum_i \lambda_{ji}c_{is}\right) \\
&= \sum_j a_{js}m_s(S_j) \\
&= s\text{th coordinate of } v(f).
\end{aligned}
$$

This completes the proof. 

**APPLICATION 1.** Let $\alpha$ be any experiment, let $\mathfrak{s} = (S_1, \cdots, S_k)$ be any partition of $X$ into $k$ disjoint $\mathfrak{B}$-measurable sets, let $P(\mathfrak{s})$ be the $n \times k$ Markov matrix with $p_{ij} = m_i(S_j)$, let $\mathfrak{P}_{\alpha k}^*$ be the range of $P(\mathfrak{s})$, and let $\mathfrak{P}_{\alpha k}$ be the set of all $n \times k$ Markov matrices $P$ which have the property $\alpha \succ P$. Then $\mathfrak{P}_{\alpha k}$ is the convex hull of $\mathfrak{P}_{\alpha k}^*$. 

This is the special case of the lemma applied to the experiment $\alpha'$ consisting of the $nk$ measures $M_{ij}$ with $M_{ij}=m_i$ for $i=1,\ldots,n$ and $j=1,\ldots,k$. Here $C$ consists of the $k$ different $n\times k$ Markov matrices $P_1,\ldots,P_k$, where $P_j$ has its $j$th column identically equal to 1 and all remaining columns identically equal to zero.

**APPLICATION 2.** For any experiment $\alpha$ and any closed bounded convex set $A$ which is the convex hull of the set of $k$ points $d_1, \cdots, d_k$, $B(\alpha, A)$ is the range of $\operatorname{diag} PD$ as $P$ varies over $\mathfrak{P}_{\alpha k}$, where $\operatorname{diag} U$ for any $n \times n$ matrix $U = \lVert u_{ij} \rVert$ denotes the n-vector $(u_{11}, u_{22}, \cdots, u_{nn})$ and $D$ is the $k \times n$ matrix whose rows are $d_1, \cdots, d_k$. 

If $C$ consists of $d_{1}, \cdots, d_{k}$ and $f$ is any decision function in $(\alpha, C)$, let $S_j=\{x:f(x)=d_j\}$ and $\mathfrak{s}=(S_1,\ldots,S_k)$. Then the $s$th coordinate of $v(f)$ is

$$
\sum_ {j} m _ {s} (S _ {j}) d _ {j s},
$$

so that 

$$
v(f) = \operatorname{diag} P(\mathfrak{s})D.
$$

Thus $B(\alpha, C)$ is the range of $\operatorname{diag} PD$ as $P$ varies over $\mathfrak{P}_{\alpha k}^{*}$. From the lemma, the convex hull of $B(\alpha, C)$ is $B(\alpha, A)$, and from Application 1 the convex hull of the range of $\operatorname{diag} PD$ as $P$ varies over $\mathfrak{P}_{\alpha k}^{*}$ is the range of $\operatorname{diag} PD$ as $P$ varies over $\mathfrak{P}_{\alpha k}$. 

**THEOREM 9.** Let $\alpha, \beta$ be two experiments with the same $n$. The following conditions are equivalent: 

(1) 

$$
\mathfrak{P}_{\alpha k} \supset \mathfrak{P}_{\beta k}.
$$

(2) For every $A$ which is the convex hull of a set of $k$ points, $B(\alpha, A) \supset B(\beta, A)$. 

(3) For every convex function $\phi$ on n-space which is the maximum of $k$ linear functions, $\int \phi\,dm_{\alpha} \geq \int \phi\,dm_{\beta}$. 

**PROOF.** Suppose (1) and let $v \in B(\beta, A)$, where $A$ is the convex hull of $d_{1}, \cdots, d_{k}$. Then $v = \operatorname{diag} PD$ for some $P \in \mathfrak{P}_{\beta k}$. 

Since $\mathfrak{P}_{\beta k} \subset \mathfrak{P}_{\alpha k}$, $v = \operatorname{diag} PD$ for some $P \in \mathfrak{P}_{\alpha k}$ and $v \in B(\alpha, A)$. Thus (1) implies (2). 

Now suppose (2) and let $P \in \mathfrak{P}_{\beta k}$. Then for any closed bounded convex set $R$, let $v \in B(P, R)$, say $v = v(f)$, where $f(j) = r_j \in R$, $j = 1, \cdots, k$. Then $v \in B(P, R^*)$, where $R^*$ is the convex hull of $r_1, \cdots, r_k$. Since $B(P, R^*) \subset B(\beta, R^*) \subset B(\alpha, R^*)$, $v \in B(\alpha, R^*)$ and consequently $v \in B(\alpha, R)$. Thus $\alpha \supset P$ for any $P \in \mathfrak{P}_{\beta k}$ and, by Theorem 8, $\alpha \succ P$. Since $\mathfrak{P}_{\alpha k}$ contains all $n \times k$ Markov matrices $P$ with $\alpha \succ P$, $P \in \mathfrak{P}_{\alpha k}$ and $\mathfrak{P}_{\beta k} \subset \mathfrak{P}_{\alpha k}$. Thus (2) implies (1). 

In considering (3), we use the fact that the standard measure $m_P$ of an $n \times k$ Markov matrix $P$ is concentrated on at most $k$ points, which follows immediately from the definition. Suppose (3), let $\phi$ be the maximum of any finite set $\mathcal{L}$ of linear functions, and let $P \in \mathfrak{P}_{\beta k}$. At each point in the support of $m_P$, select one member of $\mathcal{L}$ attaining the maximum $\phi$. The maximum $\psi$ of the selected functions uses at most $k$ members of $\mathcal{L}$ and agrees with $\phi$ on the support of $m_P$. If fewer than $k$ functions are selected, repeat any one of them; this does not change $\psi$ and puts it in the class covered by (3). Therefore

$$
\int \phi\,dm_\alpha
\geq \int \psi\,dm_\alpha
\geq \int \psi\,dm_\beta
\geq \int \psi\,dm_P
= \int \phi\,dm_P.
$$

Thus the inequality holds whenever $\phi$ is the maximum of finitely many linear functions. Every continuous convex function on the compact simplex $P$ can be approximated uniformly by maxima of finitely many affine functions. On $P$, an affine function is represented by a linear function because $\sum_i p_i=1$. Theorems 1 and 8 therefore imply $\alpha \succ P$. Hence $P \in \mathfrak{P}_{\alpha k}$, so $\mathfrak{P}_{\beta k} \subset \mathfrak{P}_{\alpha k}$ and (3) implies (1).

Finally, suppose (1) and let $\phi = \max (L_1, \cdots, L_k)$ ; say 

$$
U _ {j} = \{L _ {j} (p) = \phi (p), L _ {i} (p) <   \phi (p) \text {   for   } i <   j \}.
$$

If $S_{j} = \{p(x) \in U_{j}\}$, $\mathfrak{s} = (S_{1}, \cdots, S_{k})$ is a partition of $X$ and the experiment $P = P(\mathfrak{s})$ associated with $\beta$ and $\mathfrak{s}$ (see Application 1) has a standard measure $m_{P}$ with 

$$
m _ {P} (U _ {j}) = m _ {\beta} (U _ {j}),
$$

so that 

$$
\int \phi d m _ {\beta} = \int \phi d m _ {P}.
$$

Since $P \in \mathfrak{P}_{\beta k}$, (1) implies $P \in \mathfrak{P}_{\alpha k}$, so that $\int \phi\,dm_{\alpha} \geq \int \phi\,dm_{P} = \int \phi\,dm_{\beta}$. This completes the proof. 

If two experiments $\alpha, \beta$ with the same $n$ satisfy any of the three equivalent conditions of Theorem 9, we shall say that $\alpha$ is more informative than $\beta$ for $k$-decision problems, written $\alpha \succ_k \beta$. Condition (2) is the direct analogue of $\supset$, and condition (1) is analogous to $\succ$, since it requires that every experiment with $k$ outcomes producible from $\beta$ is also producible from $\alpha$. Clearly $\succ_{k+1}$ implies $\succ_k$, and if $\alpha \succ_k \beta$ for all $k$, then $\alpha \succ \beta$, since $\alpha \succ_k \beta$ for all $k$ implies $\int \phi\,dm_{\alpha} \geq \int \phi\,dm_{\beta}$ for every $\phi$ which is the maximum of a finite number of linear functions and hence, by approximation, for every continuous convex $\phi$. An alternative statement is: if every experiment with a finite number of outcomes which is producible from $\beta$ is also producible from $\alpha$, then $\beta$ is itself producible from $\alpha$. 

Stein (unpublished paper) has shown that in general $\succ_{k+1}$ is actually stronger than $\succ_{k}$ . For n = 2, however, all $\succ_{k}$ for $k \geq 2$ are equivalent. 

**THEOREM 10.** If $\alpha$ and $\beta$ are two experiments with $n = 2$, then $\alpha \succ_{2}\beta$ implies $\alpha \succ\beta$. 

**PROOF.** For $n = 2$, the standard measures $m_{\alpha}$ and $m_{\beta}$ are defined on the line segment $p_{i} \geq 0$, $p_{1} + p_{2} = 1$. On this line segment, every function $\phi$ which is the maximum of a finite number of linear functions is representable as $\sum a_{i}\phi_{i}$, where $a_{i} > 0$ and each $\phi_{i}$ is a maximum of two linear functions. Consequently $\alpha \succ_{2}\beta$ implies $\alpha \succ_{k}\beta$ for all $k$ and hence $\alpha \succ\beta$. 

**COROLLARY.** Let $A$ be the line segment joining $(0, 1)$ and $(1, 0)$. If $B(\alpha, A) \supset B(\beta, A)$, then $\alpha \succ \beta$. 

**PROOF.** For any line segment $A'$ in the plane, there is a transformation 

$$
\begin{aligned}
x' &= ax+b, \\
y' &= cy+d,
\end{aligned}
$$

with $LA = A'$. Since $LB(\alpha, A) = B(\alpha, LA)$ and similarly for $\beta$, we have $B(\alpha, A') \supset B(\beta, A')$, so that $\alpha \succ_2 \beta$ and consequently $\alpha \succ \beta$. 

For the $A$ of the corollary, the boundary of the set $B(\alpha, A)$ consists of two curves, joining $(0, 1)$ and $(1, 0)$, one of which is the reflection of the other about $(1/2, 1/2)$. Denote by $f_{\alpha}(t)$ the minimum of $u$ for which $(t, u) \in B(\alpha, A)$. Then $\alpha \succ \beta$ if and only if $f_{\alpha}(t) \leq f_{\beta}(t)$ for all $t$, $0 \leq t \leq 1$. The function $f_{\alpha}(t)$ is a nonincreasing convex function of $t$, representing the minimum attainable error of the second kind when the error of the first kind is fixed at $t$. Thus an alternative statement of the corollary is: 

$\alpha$ is more informative than $\beta$ if and only if at every level t the error of the second kind with $\alpha$ is less than or equal to the corresponding error with $\beta$ . 

If $\alpha \succ \beta$, then for every positive integer $r$, the experiment consisting of $r$ independent observations from $\alpha$ is more informative than the corresponding $r$-observation experiment based on $\beta$ [1]. We therefore obtain

**THEOREM 11.** If, for a sample of size 1 and every level $t$, the probability of an error of the second kind with $\alpha$ does not exceed the corresponding probability for $\beta$, then the same is true for every positive integer sample size $r$.

## REFERENCES

[1] DAVID BLACKWELL, "Comparison of experiments," Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, University of California Press, 1951, pp. 93-102. 

[2] DAVID BLACKWELL, "The range of certain vector integrals," Proc. Amer. Math. Soc., Vol. 2 (1951), pp. 390-395. 

[3] H. F. BOHNENBLUST, S. KARLIN, AND L. S. SHAPLEY, “Games with continuous convex payoff,” Contributions to the Theory of Games, Princeton University Press, 1950, pp. 181–192. 

[4] H. F. BOHNENBLUST, L. S. SHAPLEY, AND S. SHERMAN, Unpublished paper. 

[5] J. L. Doob, "Continuous parameter martingales," Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, University of California Press, 1951, pp. 269-277. 

[6] G. H. HARDY, J. E. LITTLEWOOD, AND G. POLYA, Inequalities, Cambridge University Press, 1934. 

[7] A. N. KOLMOGOROV, “Grundbegriffe der wahrscheinlichkeitsrechnung,” Ergebnisse der Mathematik, No. 3, 1933. 

[8] S. SHERMAN, "On a theorem of Hardy, Littlewood, Polya, and Blackwell," Proc. Nat. Acad. Sci., U.S.A., Vol. 37 (1951), pp. 826-831. 

[9] CHARLES STEIN, “Notes on the Comparison of Experiments,” (mimeographed), University of Chicago, 1951. 
