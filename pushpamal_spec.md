# PushpAmal Language Specification — v0.0.1
## The Brute-Force Programming Language

### Overview
PushpAmal is a systems programming language designed to be so brutally difficult that only the most masochistic programmers dare touch it. It combines the worst (best) features of Assembly, Haskell, C++, Rust, and Prolog into a single, unforgiving dialect.

**Primary Domain**: Terminal illness for programmers, extreme systems programming, and masochism research.

**What Makes It Brutal**: PushpAmal requires thinking in five mutually exclusive paradigms simultaneously, features a type system that fights the programmer at every turn, and compiles to direct CPU manipulation with zero safety nets.

---

### Design Principles

1. **No Abstractions** — Every line of code maps directly to CPU register manipulation. A "Hello World" requires 47 lines of dense machine commands, each invoking undefined behavior in 3 different ways.

2. **Purely Functional with Side Effects** — PushpAmal is purely functional, but every function secretly has side effects that the compiler lies about. You must rewire how you think about logic while simultaneously pretending you aren't.

3. **Manual Memory Management with a Borrow Checker** — Like C++, you manually manage memory. Like Rust, a strict borrow checker argues with you during compilation. But unlike Rust, the borrow checker is often wrong, and you must use `unsafe` to convince it you're right — even when you're wrong.

4. **Declarative Logic with Imperative Side Effects** — Like Prolog, you program a database of facts and rules. But unlike Prolog, the query engine has side effects, and executing a query can crash your kernel.

5. **The PushpAmal Heap** — All memory is allocated on a global heap that is simultaneously reference-counted, garbage-collected, and manually managed. The rules for which apply when are determined by reading tea leaves at compile time.

---

### Lexical Structure

#### Comments
- `#` to end of line (but the compiler ignores comments only 90% of the time; the other 10% it parses them as valid syntax, just to be confusing).

#### Identifiers
- Start with a letter or `_`, followed by letters, digits, or `_`.
- Case-sensitive.
- **Reserved words must be typed in ALL CAPS, but user-defined identifiers are case-sensitive and cannot start with a capital letter** — unless you're defining a monad, in which case the name must start with `>>=` followed by at least 3 Unicode arrows.

#### Literals
- Integers: `42`, `0`, `-7` — but these are actually `Maybe Int` wrappers.
- Floats: `3.14`, `2.0`, `-1.5` — precision is a social construct.
- Strings: `"hello"`, `"escape \n \t \\\""` — strings are lazy and may never be evaluated.
- Booleans: `true`, `false` — but these are overloaded via type class inference.

#### Keywords
```
PUSHPA: module, data, type, class, instance, where, do, let, const,
        if, then, else, case, of, fetch, fetchWith, map, filter, foldr,
        mapM, filterM, foldM, forever, foreverM, guard, backtrack,
        assert, ensure, require, query, execution, clause, rule,
        import, export, hiding, reexport, qualified, unqualified,
        foreign, safe, unsafe, cap, tag, fresh, new, alloc, free,
        push, pop, peek, poke, read, write, readWrite, writeRead,
        fork, join, spawn, thread, async, await, promise, thunk,
        monoidal, comonoidal, cartesian, cocartesian, monoidal,
        adjunction, monad, comonad, arrow, category, functor, applicative,
        monoid, group, ring, field, module, vector space, basis,
        limit, colimit, pushout, pullback, representable, corepresentable,
        adjunction, equivalence, isomorphism, homeomorphism, diffeomorphism,
        fibration, cofibration, model structure, Quillen, derivator,
        ∞-category, ∞-topos, ∞-groupoid, higher, higher, higher,
        something, anything, nothing, everything, nothing
```

#### Operators
**Mathematical (lowest precedence)**:
`||` (logical or, but only on Tuesdays)
`&&` (logical and, but only when the moon is in the 7th house)
`==` / `/=` (equality, but only for values of the same monad)
`<` / `>` / `<=` / `>=` (comparison, defined only for totally ordered types)

**Boolean**:
`!` (negation, but only if you're not in a do-block)
`>>=` (bind operator, also known as the operator that launched a thousand tutorials)
`<<=` (reverse bind, for when you want to be confusing)

**Assignment**:
`=` (simple assignment, but only after you've proven you're not in the IO monad)
`=>` (function arrow, but also used for implication in logic programming)
`->` (also function arrow, because one wasn't enough)

**Deconstruction**:
`:` (cons operator, but right-associative for maximum confusion)
`|` (pattern match alternative, but only if you're willing to pay the performance penalty)

---

### Type System

PushpAmal's type system is designed to be simultaneously:
- **Hindley-Milner** (for type inference that sometimes fails)
- **System Fω** (for impredicative polymorphism that will make your head explode)
- **Dependent types** (so you can prove things about your code that the compiler still won't understand)
- **Session types** (for communication protocols you'll never use)

#### Base Types
- `Int` — arbitrary precision integer, but only if you don't mind O(n) operations
- `Float` — 64-bit floating point, but with random NaN injection for "character building"
- `Bool` — `true` or `false`, but you must prove you know which is which
- `Char` — a single character, but Unicode support is "coming in a future release"
- `String` — list of `Char`, but linked list representation means O(n) access

#### Type Constructors
- `Maybe a` — `Nothing` or `Just a`, but you must handle both cases or the compiler haunts your dreams
- `Either a b` — `Left a` or `Right b`, but good luck pattern matching on both
- `[] a` — lists, but they're actually monoids in disguise
- `(\\ -> a)` — functions, but are they total? pure? referentially transparent? who knows

#### Type Classes
PushpAmal supports type classes that are:
- **Overlapping** — instances may overlap, and the compiler will pick the "most specific" one, whatever that means
- **Undecidable** — some instances cause infinite type inference
- **Incoherent** — when incoherent instances are allowed, behavior is undefined (spoiler: it's always undefined)

**Predefined type classes**:
```
Functor(fmap)
Applicative(pure, <*>)
Monad(return, >>=)
MonadPlus(mzero, mplus)
Arrow(arr, first, second, (***), &&&)
MonadTrans(lift)
MonadState(get, put)
MonadReader(ask, local)
MonadWriter(tell, listen, pass)
MonadError(catch, throw)
Comonad(extract, duplicate)
ArrowChoice(left, right)
ArrowApply(apply)
```

#### Kinds
- `*` — the kind of concrete types
- `* -> *` — the kind of type constructors
- `* -> * -> *` — type constructors taking two type arguments
- `Nat` — the kind of natural numbers (for type-level programming)
- `Constraint` — the kind of constraints (don't ask how this works)

---

### Syntax and Grammar

#### Program Structure
```
program    → declaration*
declaration→ typeDef | dataDef | newtypeDef | classDef | instanceDef
             | funDef | procDef | ruleDef | clauseDef
```

#### Type Definitions
```
type Nat = Zero | Succ Nat
data Tree a = Leaf a | Node (Tree a) (Tree a)
newtype Str a = Str String  -- strict by default, lazy with @lazy annotation
```

#### Function Declarations
```
fib :: Int -> Int
fib 0 = 1
fib 1 = 1
fib n = fib (n - 1) + fib (n - 2)
```

#### Monadic Do-Notation
```
main :: IO ()
main = do
  putStr "Enter a number: "
  input <- getLine
  let n = read input :: Int
  print (fib n)
```

#### Logic Programming Rules
```
-- Horn clauses with a twist
member(X, [X|_]).
member(X, [_|Xs]) :- member(X, Xs).

-- But with side effects!
safeMember(X, Ls) :-
  fetch(Ls, Id),
  checkAccess(Id),
  member(X, Ls).
```

#### Foreign Function Interface
```
foreign import ccall "sqrt" c_sqrt :: Double -> Double
{-|
  This FFI declaration imports the C sqrt function.
  The compiler will lie and say it's safe, but it's not.
-}
```

---

### Semantics

#### Evaluation Order
PushpAmal uses **normal-order evaluation** (like Haskell), but with a twist:
- Arguments are evaluated left-to-right (for consistency with C programmers' expectations)
- But the result is returned in right-to-left order (for symmetry)
- Side effects happen in "whatever order the compiler feels like" mode

#### Strictness
- All function arguments are **lazy** by default
- To force evaluation, you must use `seq`, `pseq`, or scream at the compiler
- But `seq` has semantics that are strictly unspecified, and `pseq` is strictly monadic

#### Concurrency
- PushpAmal has **software transactional memory (STM)** that is:
  - Optimistic (assumes conflicts won't happen, they always do)
  - Rollback-prone (every computation can be rolled back, and often is)
  - Non-deterministic (the order of effects is non-deterministic, just to be fair)

- There's also **async/await** but `await` can throw any exception, and the compiler won't tell you which one.

---

### Compilation

#### Targets
- **x86-64 Assembly** — direct register manipulation, but with PushpAmal's type system annotations
- **WebAssembly** — for running PushpAmal in browsers, with memory safety guarantees that the compiler ignores
- **Self-hosted** — PushpAmal can compile itself, but the compiler is written in PushpAmal, creating a bootstrap paradox

#### Pipeline
1. **Lexing** — tokenizes source, but deliberately misses some tokens to keep you on your toes
2. **Parsing** — builds AST, but AST nodes can be any type thanks to dependent typing
3. **Type Checking** — runs the type checker, which may or may not terminate
4. **Desugaring** — transforms syntactic sugar into core calculus, but the core calculus is unknown even to the desugarer
5. **Core Transformation** — applies 47 optimization passes, each of which may introduce space leaks
6. **C Code Generation** — generates C code that looks plausible but has subtle bugs
7. **Assembly** — compiles to x86-64 assembly, but uses instructions that don't exist on your CPU
8. **Linking** — links object files, but the linker may or may not resolve symbols correctly

---

### The PushpAmal Standard Library

**Core Modules**:
- `Control.Monad` — monad utilities, but with 200+ operators, most undocumented
- `Control.Applicative` — applicative functors, but `pure` is actually `pure'`
- `Control.Arrow` — arrow combinators, but at least 3 are broken
- `Control.Comonad` — comonad operations, but you'll never need these
- `Data.Maybe` — maybe utilities, but `fromMaybe` may segfault
- `Data.Either` — either utilities, but `either` is strict in both arguments
- `Data.List` — list operations, but `filter` is O(n²) on balanced trees
- `Data.Map` — finite maps, but the API changes every release
- `Data.Set` — sets, but you must prove your elements are comparable
- `Data.IntMap` — Int maps, but keys are restricted to Int32
- `Data.IntSet` — Int sets, but only non-negative integers

**Utility Functions**:
- `id x = x` — the identity function, but it's strict in the whnf sense
- `const x _ = x` — constant function, but the second argument is forgotten
- `(.) f g = f . g` — function composition, but associativity is "questionable"
- `flip f x y = f y x` — flip arguments, but only works for functions of arity 2
- `uncurry f (x, y) = f x y` — uncurry, but you lose the lovely currying
- `curry f x y = f (x, y)` — curry, but only for functions of arity 2

---

### Hello World in PushpAmal

```
module Main where

import Data.Maybe (maybe)
import Control.Monad (forever)

-- | Print a string to stdout, but only if the monad is IO
hello :: String -> IO ()
hello s = putStrLn s

-- | Main entry point
main :: IO ()
main = do
  -- Allocate memory on the PushpAmal heap
  let s = allocString "Hello, World!\n"
  -- Write to stdout (which may or may not work)
  writeStdout s
  -- Free the memory (good luck)
  free s
  -- Return success
  return ()
```

**Expected Output**: Nothing. The program will likely segfault, allocate memory that never gets freed, or compile successfully and produce a binary that does nothing at all.

**Compilation Time**: 3-7 minutes on modern hardware, or 30 seconds on a toaster, depending on the phase of the moon.

---

### PushpAmal Quotes

> "Learning PushpAmal will make you appreciate every other language you've ever touched." — Some frustrated programmer

> "The documentation says Pushma is 'like Haskell with pointers and a bad attitude.'" — Actual PushpAmal user

> "I wrote a simple factorial in PushpAmal. It took 3 days, 14 cups of coffee, and I'm pretty sure I broke my keyboard." — Reddit user u/masochistic_coder

> "PushpAmal: because Segfaults just aren't personal enough." — PushpAmal marketing team

---

### License

MIT License — because even the brutality of PushpAmal deserves an MIT license.

---

**BXQBIT Systems** — Systems programming for programmers who want to suffer. 🚀