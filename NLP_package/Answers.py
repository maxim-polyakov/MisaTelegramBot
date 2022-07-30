import NLP_package

class Answer:

    def answer(self):
        pass

class RandomAnswer(Answer):
    
    conn = NLP_package.psycopg2.connect("dbname=postgres user=postgres password=postgres")

    inpt = NLP_package.pd.read_sql('SELECT * FROM hiset', conn)

    data = NLP_package.pd.concat([inpt])
    df = []

    def answer(self):

        for i in range(0, len(self.data['text'])-1):
            if(self.data['hi'][i] == 1):
                self.df.append(self.data['text'][i])
     #  print(self.df)
        outmapa = {0: [self.df[NLP_package.random.randint(0, len(self.df))]]}
                
        return (outmapa[0])
