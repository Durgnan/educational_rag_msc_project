from rag import AdvancedRAG
from ragas import evaluate
from ragas.run_config import RunConfig
from ragas.metrics import ( answer_relevancy, faithfulness, context_recall, context_precision )
from datasets import Dataset
from dotenv import load_dotenv
from langchain_community.llms import Ollama
load_dotenv()


class Test:
    def __init__(self, model:str = "llama3"):
        self.rag = AdvancedRAG(model=model, db="faiss_db_900")
        contexts = []
        questions = [
            "How much space does the recursive algorithm for computing the nth Fibonacci number F(n) use?",
            "Write an algorithm for computing x^n in log2n steps, for any n (including when n is not a power of 2). Your answer should include code or pseudocode for the algorithm, and a demonstration that it takes at most log2n steps",
            "(i) Show that if f(n) = O(g(n)) then g(n) = Ω(f(n)).(ii) What would be the equivalent for oand ω?(iii) What would be the equivalent Θ?(iv) Is it possible to find a function f(n) that is o(g(n)) and ω(g(n))?",
            "Show that the recursive algorithm for computing the nth Fibonacci number F(n) takes Θ(F(n))steps to run."
        ]
        answers = [ 
            ['''Program uses a fixed amount of space for each entry in the functioncall stack. The stack never has more than nentries, because F(n) calls F(n−1), which callsF(n−2), and so on until F(2). So the space used is Θ(n).'''],
            [''' Consider x^5. Write it as x^4 . x^1= (x^2)^2 . x^1. Note that in binary, 5 = 0b101 = 1 · 2^2 + 0 · 2^1 + 1 · 2^0. Want to store the result as y, so start with y= 1. Start with z=x^1. We want to include this in final value for y so we compute y←y×z=x. Now compute z←z∗z=x^2. We don’t want an x^2 term in y so we just leave y as it is. Now compute z←z×z=x^4. We do want the x^4 term in y so we compute y←y×z=x1×x^4 = x^5 and we’re done.The following Python code will do it:
                def power(x, n):
                    y=1
                    while n:
                        if n & 1:       # extract last bit of n
                            y = y*x
                        n = n >> 1      # shift n to the right
                        x = x*x
                    return y
                
                There at most log2n nonzero bits in the binary representation of n so it takes less than log2nsteps.
            '''],
            ['''
                (i) f(n) = O(g(n)) means that there are constants c, n0 so that for n≥n0, 0 ≤f(n)≤cg(n). So 0≤(1/c)f(n)≤g(n)
                This is the definition of g(n) being Ω(f(n)) with 1/c instead of c as the constant.
                (ii) f(n) = o(g(n)) if and only if g(n) = ω(f(n)).
                (iii) f(n) = Θ(g(n)) if and only if g(n) = Θ(f(n)).
                (iv) No!
                    If f(n) = o(g(n)) then for all c > 0 you can find n0 so that if n≥n0 then f(n)< cg(n). Write n0+(c) for this n0.
                    If f(n) = ω(g(n)) then for all c > 0 you can find n0 so that if n≥n0 then f(n)> cg(n). Write n0-(c) for this n0.
                    Given c, if n≥max(n+0(c), n0-(c)) then f(n)> cg(n) and f(n)< cg(n), which can’t happen.
            '''],
            ['''
                We will show it takes g(n) = 2F(n)−1 steps.
                Step 1: obviously true for n= 1,2.
                Step 2: assume it is true for all n < N when N > 2. Try to show it is true for N.
                Then we are in the else condition, and so it takes the number of steps for fib_recurse(N-1) plus the number of steps for fib_recurse(N-2) plus 1.
                That is:
                    g(N) = g(N−1) + g(N−2) + 1
                         = (2F(N−1) −1) + (2F(N−2) −1) + 1
                         = 2F(N)−1
                So true for N. By induction we have shown it is true for all N.
            ''']
        ]
        rag_answers = []
        
        
        for question in questions:
            rag_answers.append(self.rag.answer_question(question))
            contexts.append([docs.page_content for docs in self.rag.retriever.get_relevant_documents(question)])
            
        self.dataset = Dataset.from_dict({
            "contexts": contexts,
            "question": questions,
            "answer": rag_answers,
            "ground_truths": answers
        })
        
    def test(self):
        langchain_llm = Ollama(model="llama3")
        result = evaluate(
            dataset = self.dataset,
            llm=langchain_llm,
            embeddings=self.rag.embeddings,
            metrics=[
                context_precision,
                faithfulness,
                answer_relevancy,
                context_recall,
            ],
            run_config=RunConfig(max_workers=64)
        )
        print(result)
        df = result.to_pandas()
        df.head()
        df.to_csv("test.csv")
        # return df


if __name__ == "__main__":
    test = Test()
    test.test() 
    