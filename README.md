# AMM_prototype

**Presentation Slide Show For Research Project:**
https://github.com/brynchristineloftness/AMM_prototype/blob/master/Explanation_SlideShow.pdf

**Background of Prototype:**

This repository is a prototype I am currently designing for Washington State University to merge redundant automatically generated tests with pre-existing manually written tests from a given test suite. The goal of the merge prototype is to present to a programmer pairs of similar test cases within their test suite to potentially remove or modify to improve speed, efficiency, and overall design. This project started during an REU I participated in this summer of 2020 alongside WSU doctoral student, Devjeet Roy, under the advisement of Dr. Venera Arnaoudova. I was recruited for the research team due to my background in natural language processing and information retrieval. This was an opportunity to explore and improve my abilities with the technologies I was familiar with within a totally new arena (source code analysis versus biological data analysis). The REU program ended in July, however I have continued to work on polishing the prototype to potentially publish with Dr. Venera and Devjeet in the coming months. They have allowed me to work very independently to design this code base and algorithm. 

**General Description of Prototype Algorithm:**

The algorithm I have designed to isolate similar test cases is based on several key heuristics I have identified by manually analyzing test cases we have labeled as similar and removeable from a given suite. Some of these heuristics are similar Assert statements, similar Methods being tested, and overall keyword order and presence. The structure can be largely compared to a decision tree isolating those key heuristics using techniques within dynamic programming, information retrieval, and natural language processing. I call my algorithm the “Pack n Prune” approach. In short, I create large generalized clusters of potential matches based on broad similarity metrics that all similar test cases fall into, I then incrementally divide this generalized cluster into a decision tree of smaller clusters of test cases based on the previously mentioned heuristics. I then prune from these smaller clusters to isolate the key test cases for merging using various procedures depending on the heuristic. 

**Current Status of Prototype:**

Currently the prototype is still in the testing/construction. It has been designed on one test suite, and needs to be combined with another code base (from Devjeet Roy) to allow for streamlined testing with additional test suites. 
