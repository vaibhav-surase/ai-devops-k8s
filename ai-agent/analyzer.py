import os
from dotenv import load_dotenv
from kubernetes import client, config
from openai import OpenAI

load_dotenv()

config.load_kube_config()

v1 = client.CoreV1Api()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_pods():

    pods = v1.list_pod_for_all_namespaces()

    for pod in pods.items:

        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name
        phase = pod.status.phase

        print("=" * 60)
        print("Pod:", pod_name)
        print("Namespace:", namespace)
        print("Status:", phase)

        if phase != "Running":

            try:
                logs = v1.read_namespaced_pod_log(
                    name=pod_name,
                    namespace=namespace
                )
            except Exception as e:
                logs = str(e)

            prompt = f"""
You are a Kubernetes DevOps troubleshooting assistant.

Analyze this Kubernetes issue.

Pod:
{pod_name}

Namespace:
{namespace}

Status:
{phase}

Logs:
{logs}

Provide:

1. Problem
2. Likely root cause
3. Evidence
4. Troubleshooting steps
5. Recommended fix
6. Prevention
"""

            response = openai_client.responses.create(
                model="gpt-5.5",
                input=prompt
            )

            print("\nAI ANALYSIS:\n")
            print(response.output_text)


if __name__ == "__main__":
    analyze_pods()
