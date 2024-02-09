# import packages
import argparse
import os
from kfp import dsl
from kfp import compiler
from google.cloud import aiplatform

# define environment variables
GCP_PROJECT = "ac215-399020"
GCS_BUCKET_NAME = "rehab-image-detection-pipeline"
GOOGLE_APPLICATION_CREDENTIALS = "../secrets/gcp-rehab-ai-secret.json"
GCP_REGION = "us-central1"
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root"
GCS_PACKAGE_URI = f"{BUCKET_URI}/pipeline_root/packages"
LOCATION = "us-central1"
SERVICE_ACCOUNT = "rehab-ai@ac215-399020.iam.gserviceaccount.com"


# define container images
@dsl.container_component
def data_scraping_spec():
    return dsl.ContainerSpec(
        image='us-central1-docker.pkg.dev/ac215-399020/vertex-ai-pipeline/c1-data-scraping:latest'
    )


@dsl.container_component
def data_preprocessing_spec():
    return dsl.ContainerSpec(
        image='us-central1-docker.pkg.dev/ac215-399020/vertex-ai-pipeline/c2c-data-preprocessing:latest'
    )


@dsl.container_component
def model_training_spec():
    return dsl.ContainerSpec(
        image='us-central1-docker.pkg.dev/ac215-399020/vertex-ai-pipeline/c3-model-training:latest'
    )


# define whole pipeline
@dsl.pipeline(
    name='Run all components',
    description='Runs the entire pipeline.'
    )
def whole_pipeline():
    data_scraping_spec()
    data_preprocessing_spec()
    model_training_spec()
    print("Pipeline defined.")


# compile whole pipeline
def compile_whole_pipeline():
    compiler.Compiler().compile(
        pipeline_func=whole_pipeline,
        package_path='whole_pipeline.yaml'
        )
    print("Compiled pipeline yaml successfully!")


# initialize vertex ai
def initialize_vertex_ai():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
    aiplatform.init(project=GCP_PROJECT, location=LOCATION)
    print("Initialized Vertex AI successfully!")


# upload pipeline to vertex ai
def upload_pipeline_to_vertex(pipeline_path):
    initialize_vertex_ai()

    pipeline = aiplatform.PipelineJob(
        display_name="rehab-ai-pipeline",
        template_path=pipeline_path,
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    pipeline.run(service_account=SERVICE_ACCOUNT)
    print("Uploaded job to Vertex AI successfully!")


# CLI functionality
def main():
    parser = argparse.ArgumentParser(description='Execute Kubeflow Pipelines')

    # Add arguments
    parser.add_argument('-scrape', action='store_true', help='Execute only the data scraping pipeline')
    parser.add_argument('-preprocess', action='store_true', help='Execute only the data preprocessing pipeline')
    parser.add_argument('-train', action='store_true', help='Execute only the model training pipeline')
    parser.add_argument('-all', action='store_true', help='Execute the entire pipeline')
    
    # Parse arguments
    args = parser.parse_args()
    if args.scrape:
        print("Executing only the scraping component...")
        # TODO: Compile and upload the scraping pipeline
        
    if args.preprocess:
        print("Executing only the preprocess component...")
        # TODO: Compile and upload the preprocessing pipeline

    if args.train:
        print("Executing only the training component...")
        # TODO: Compile and upload the training pipeline

    elif args.all:
        print("Executing the entire pipeline...")
        # Compile the pipeline
        compile_whole_pipeline()

        # Upload the pipeline
        upload_pipeline_to_vertex('whole_pipeline.yaml')


if __name__ == '__main__':
    main()
