source venv/bin/activate
python -c "
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('PAGERDUTY_USER_API_KEY', 'NOT SET')
api_host = os.getenv('PAGERDUTY_API_HOST', 'https://api.pagerduty.com')

print(f'API Key: {api_key[:10]}...' if len(api_key) > 10 else f'API Key: {api_key}')
print(f'API Host: {api_host}')

try:
    response = httpx.get(
        f'{api_host}/services',
        headers={
            'Authorization': f'Token token={api_key}',
            'Content-Type': 'application/json'
        },
        params={'limit': 1},
        timeout=10
    )
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ PagerDuty connection working!')
    else:
        print(f'Response: {response.text[:300]}')
except Exception as e:
    print(f'Error: {e}')
"


{
  "mcpServers": {
    "confluence": {
      "command": "mcp-atlassian-confluence",
      "args": [],
      "env": {
        "ATLASSIAN_SITE_NAME": "your-company",
        "ATLASSIAN_USER_EMAIL": "your.email@company.com",
        "ATLASSIAN_API_TOKEN": "your_api_token_here"
      },
      "disabled": false
    }
  }
}



























Networking & Security1. What is the primary difference between a Security Group and a Network ACL (NACL) in an AWS VPC?Answer: A Security Group acts as a virtual firewall for your instance and is stateful (it automatically allows return traffic). A Network ACL acts as a firewall for the subnet and is stateless (you must explicitly define both inbound and outbound rules).2. How would you allow an ECS task in a private subnet to securely download updates from the internet?Answer: You must route the traffic through a NAT Gateway located in a public subnet. This allows outbound internet access for resources in a private subnet while preventing the internet from initiating a connection with those resources.3. When connecting two VPCs, when would you choose VPC Peering over a Transit Gateway?Answer: VPC Peering is best for a simple, 1-to-1 connection between two VPCs with low complexity. Transit Gateway is preferred for a "hub-and-spoke" architecture connecting multiple VPCs and on-premises networks, as it simplifies management and routing at scale.Compute & Containers4. In an AWS ECS environment, what is the role of Amazon ECR?Answer: Amazon ECR (Elastic Container Registry) is a fully managed Docker container registry used to store, manage, and deploy Docker container images that are then pulled by ECS or EKS for execution.5. How do you ensure "Zero-Downtime" when deploying a new version of a microservice to an ECS Cluster?Answer: Use a Rolling Update or Blue/Green deployment strategy. By setting the minimumHealthyPercent to 100%, ECS will ensure new tasks are healthy and passing target group health checks before draining and stopping the old versions.6. For a high-performance database like ClickHouse or PostgreSQL on AWS, would you use Instance Store or EBS volumes?Answer: For temporary, high-speed cache or "scratch" data, Instance Store is faster. However, for persistent data like PostgreSQL or ClickHouse production databases, EBS (Elastic Block Store) is required because it persists data independently of the instance's life cycle and supports snapshots/backups.Data Services & Analytics7. What are the advantages of using Amazon Athena for querying data stored in S3 compared to a traditional RDS instance?Answer: Athena is a serverless, interactive query service that allows you to run standard SQL directly against data in S3. It requires no infrastructure management and you only pay for the queries you run, making it ideal for ad-hoc analysis of logs or large datasets.8. How do you handle schema evolution in a data lake environment where you use AWS Glue and Athena?Answer: You use the AWS Glue Crawler to automatically scan your S3 data, detect the schema, and update the Glue Data Catalog. Athena then uses this catalog to reflect the new columns or data types in your SQL queries.Infrastructure as Code (IaC) & CI/CD9. Why is it considered a best practice to use Terragrunt alongside Terraform for managing multi-environment AWS infrastructure?Answer: Terragrunt keeps your Terraform code "DRY" (Don't Repeat Yourself) by allowing you to define remote state configurations and provider blocks in one place and inherit them across multiple environments (Dev, Stage, Prod), reducing configuration drift.10. How can AI-assisted workflows (e.g., Claude Code or GitHub Actions) improve the reliability of a DevOps pipeline?Answer: AI tools can be used for automated code reviews, identifying security vulnerabilities in IAM policies before they are deployed, and generating infrastructure testing scripts to validate that a deployment meets SLI/SLO metrics.Summary of Skills EvaluatedAreaFocus SkillNetworkingVPC Architecture & SecurityComputeECS/ECR & Deployment StrategiesData ServicesAthena & RDS ManagementAutomationTerraform, Terragrunt, & AI-Led Dev
