# ResilienceBench: A Resiliency Pattern Benchmark

ResilienceBench is a language-agnostic benchmark environment to support the experimental evaluation of microservice resiliency patterns, such as [Retry](https://docs.microsoft.com/en-us/azure/architecture/patterns/retry) and [Circuit Breaker](https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker), using open source resilience libraries, such as C\#'s [Polly](https://github.com/App-vNext/Polly) and Java's [Resilience4j](https://github.com/resilience4j/resilience4j). 

![Build status](https://github.com/ppgia-unifor/resilience-bench/actions/workflows/docker-image.yml/badge.svg)

Jump to:


* [Documentation](/docs)

* [Installation instructions](docs/installation.md)

* [Demo video](#demo-video)

* [Publications](#publications)

* [Credits](#credits)

## Demo video

This short (2m:20s) video provides a quick overview of the steps necessary to install, configure, and run resilience tests with ResilienceBench. 

[<img src="docs/img/video-thumbnail.jpg" width=500>](https://www.youtube.com/watch?v=X7nzlK86eAo "ResilienceBench Demo Video")

## Publications

Costa, T. M., Vasconcelos, D. M., Aderaldo, C. M., and Mendonça, N. C. (2022). [Avaliação de Desempenho de Dois Padrões de Resiliência para Microsserviços: Retry e Circuit Breaker](publications/sbrc2022-final.pdf). In 40th Brazilian Symposium on Computer Networks and Distributed Systems (SBRC 2022). The experimental dataset used in this paper is available in the [/data/sbrc2022](data/sbrc2022/) folder.

Aderaldo, C. M., and Mendonça, N. C. (2022). [ResilienceBench: Um ambiente para avaliação experimental de padrões de resiliência para microsserviços ](). In 40th Brazilian Symposium on Computer Networks and Distributed Systems (SBRC 2022). The version presented in the conference and described in the paper is available [here](publications/sbrc_tools_2022.pdf).


## Credits

ResilienceBench is being developed by [Carlos M. Aderaldo](https://github.com/cmendesce) and [Nabor C. Mendonça](https://github.com/nabormendonca), from University of Fortaleza (UNIFOR), Brazil, in collaboration with [Javier Cámara](https://javier-camara.github.io/), from University of Málaga, Spain, and [David Garlan](http://www.cs.cmu.edu/~garlan/), from Carnegie Mellon University (CMU), USA.

