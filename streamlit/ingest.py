import boto3, time, os


def start_ingestion_job(knowledge_base_id, data_source_id):
    # Initialize the AgentsforBedrock client
    client = boto3.client("bedrock-agent")

    # Start the ingestion job
    response = client.start_ingestion_job(
        # clientToken="your_client_token",
        dataSourceId=data_source_id,
        # description="your_description",
        knowledgeBaseId=knowledge_base_id,
    )

    # Return the ingestion job ID
    return response["ingestionJob"]["ingestionJobId"]


def get_ingestion_job(knowledge_base_id, data_source_id, ingestion_job_id):
    # Initialize the AgentsforBedrock client
    client = boto3.client("bedrock-agent")

    # Get the ingestion job
    response = client.get_ingestion_job(
        dataSourceId=data_source_id,
        ingestionJobId=ingestion_job_id,
        knowledgeBaseId=knowledge_base_id,
    )

    # Return the ingestion job details
    return response["ingestionJob"]


def ingest_and_confirm(knowledge_base_id, data_source_id):
    # Start an ingestion job
    ingestion_job_id = start_ingestion_job(knowledge_base_id, data_source_id)

    while True:
        # Get the status of the ingestion job
        ingestion_job = get_ingestion_job(
            knowledge_base_id, data_source_id, ingestion_job_id
        )

        # If the status is 'COMPLETE', break the loop
        if ingestion_job["status"] == "COMPLETE":
            print("Ingestion job is complete.")
            break

        # If the status is not 'COMPLETE', wait for a while before checking again
        else:
            time.sleep(5)


def main():
    # Replace these with your actual knowledge base ID and data source ID
    knowledge_base_id = "RL7V0ZUTI6"
    data_source_id = "ADIAXAKE25"

    # Call the new function
    ingest_and_confirm(knowledge_base_id, data_source_id)


if __name__ == "__main__":
    main()
