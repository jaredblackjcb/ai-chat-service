import os
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.memory import ChatMessageHistory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

class PineconeUtils():
    
    def __init__(self, namespace, context):
        self.namespace = namespace
        self.context = context
        self.index = os.environ.get('PINECONE_INDEX')
        pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'),
                    environment=os.environ.get('PINECONE_ENV'))
        
    def get_reply(self, query):
        # Get previous message context as a ConversationBufferMemory
        memory = self._generate_chat_memory()

        # Access the Pinecone vector store associated with the user's namespace
        embeddings = OpenAIEmbeddings()
        vector_store = Pinecone.from_existing_index(index_name=self.index, embedding=embeddings, namespace=self.namespace)

        # Set up the model and retriever
        # Setting temperature to 0 removes some of the randomness of 
        # responses and reduces hallucination, so is good for data extraction
        llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
        retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})

        # Create and run a converstation chain
        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, memory=memory)
        answer = chain.run(query)
        return answer
        # loader = TextLoader('./documents/postgres.txt')
        loader = DirectoryLoader(directory)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            # length_function=??? # TODO: Define Function that measures the length of given chunks in tokens
            )
        chunks = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        # Generate document vectors and automatically upsert them into Pinecone
        vector_store = Pinecone.from_documents(chunks, embeddings, index_name=self.index, namespace=namespace)

    # Generate a ConversationBufferMemory to provide context using all previous messages
    # Docs: https://python.langchain.com/docs/modules/memory/agent_with_memory_in_db
    # TODO: [FEATURE] Add RedisChatMesssageHistory to retrieve past conversations from database
    def _generate_chat_memory(self):
        # Loop through all the messages sent from the chat widget and add them to message history
        message_history = ChatMessageHistory()
        for message in self.context:
            if message['type'] == 'bot':
                message_history.add_ai_message(message['message'])
            else:
                message_history.add_user_message(message['message'])
        
        # Create the memory to provide context for the new query
        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=message_history)
        return memory


