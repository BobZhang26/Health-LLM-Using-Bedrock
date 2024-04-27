## Using Amazon Bedrock Knowledge Bases

This project implements a contextual chatbot application built on Amazon Bedrock Knowledge Bases using Retrieval-Augmented Generation (RAG).

### Technical Specifications:

* Knowledge Base Name: knowledgebase-</your-awsaccount-number/>
* Embedding Model: Titan Embedding G1 – Text.
* Foundation Model: Anthropic Claude
* Vector Database: Amazon Opensearch Severless vector
* AWS Cloud Formation to deploy lambda function for retrival

### Project Dependencies:

Refer to a requirements.txt file (or equivalent) outlining all necessary libraries and their versions.

### Prerequisites:

* An AWS account with access to Amazon Bedrock services.
* Local development environment with Python and access to AWS CLI.
* Data Preparation:
    Organize your chatbot's knowledge base content (documents, FAQs) by uploading the documents in a AWS S3 bucket.
    Ensure data format compatibility with Amazon Bedrock (e.g., text files, pdfs).

### Knowledge Base Creation:

* Create bucket.
* Name the bucket knowledgebase-</your-awsaccount-number/>.
* Choose Create folder and name it dataset, upload documents here.
* Specify the data source location containing your knowledge base content 
* For Embeddings model, select Titan Embedding G1 – Text.
* For Vector database, you can either select Quick create a new vector store or Choose a vector store you have created and then sync.

### Lambda function Creation:

* Create folder in the originally created s3 bucket and name it lambdalayer.
* Upload the knowledgebase-lambdalayer.zip file available under the /lambda/layer folder in this repo and upload.
* On the AWS CloudFormation service home page, create a stack.
* Upload the .yaml file under the cfn folder as a template file to create the stack
* Choose the appropriate knowledge ID from your created knowledge base and also the LambdaLayers3bucket name where the lambda layer code was uploaded earlier.
* SUbmit and Verify that the CloudFormation template ran successfully.

## Test function Locally

* Clone the repository
* Create environment and pip install requirements.txt file
* Navigate to the /streamlit folder.
* Run the following command to instantiate the chatbot application:
```
python -m streamlit run chatbot.py
```
