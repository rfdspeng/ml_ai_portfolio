# DevOps

Integrates and automates the processes between software dev (Dev) and IT operations (Ops) to get faster and more reliable software delivery.
* Uses automation to streamline processes, reduce manual errors, and speed up dev lifecycle
* CI/CD (continuous integration and delivery): code changes are frequently integrated into a shared repo, and software is automatically deployed (delivered) to production
* Monitors applications and infrastructure to quickly identify issues and provide feedback for improvement
* Uses IaC (infrastructure as code) to allow for consistent and repeatable deployments

Why?
* Automation allows for faster software delivery
* Continuous integration, testing, and feedback loops identify and resolve issues earlier in the dev lifecycle, producing higher-quality software
* Monitoring improves software reliability and stability


https://aws.amazon.com/devops/what-is-devops/

DevOps practices:
* Very frequent but small updates - more incremental than the occasional updates performed under traditional release practices. This makes each deployment less risky and allows for faster bug fixes.
* May also use a microservices architecture for flexibility. In a microservices architecture, complex applications are broken into simple individual components (services) with each service scoped to a single purpose or function and operated independently of its peer services and the application as a whole. This reduces the coordination overhead of updating applications.
* However, the combination of microservices and increased release frequency means significantly more deployments, which can present operational challenges. That's why we need DevOps practices like CI/CD, infrastructure automation like infrastructure as code (IaC) and configuration management, and monitoring and logging of deployed applications.

Let's get specific:
* _Continuous integration (CI)_: devs regularly merge code changes into a central repo, after which automated builds and tests are run. The goal of this is to find and address bugs more quickly, improve sw quality, and reduce the time it takes to validate and release new sw updates.
* _Continuous delivery (CD)_: code changes are automatically built, tested, and prepared for a release to production. Expands on CI by deploying all code changes to a testing environment and/or production environment after build so that devs will always have a deployment-ready build artifact that has passed through a standardized test process.
* _Microservices_: build a single application as a set of small services. Each service runs in its own process and communicates with the others, typically an HTTP-based API.
* _Infrastructure as code_: infrastructure is provisioned and managed using code and sw dev techniques like version control and CI, just like application code. For example, AWS provides the AWS CLI or Python SDK boto3 for this purpose. Compared to manual provisioning, IaC means infrastructure and servers can quickly be deployed using standardized patterns, updated, and duplicated.
    * _Configuration management_: similarly, dev and sysadmin can use code to configure infrastructure, like OS, system applications, or server software
    * _Policy as code_: same thing but for security policies governing access
* _Monitoring and logging_: monitoring metrics and logs to see how app/infra performance or changes to app/infra affect the user experience. Active monitoring becomes increasingly important as services must be available 24/7 and app/infra update frequency increases. Creating alerts and performing real-time analysis of the logs.


I think operations is about operating (deploying, monitoring) the software? Dev is about dev the software, obviously.

It's not just infrastructure and operations; it's also dev. DevOps.

Examples of microservice arch?

IaC - using AWS SDK or CLI to provision cloud resources is NOT IaC. AWS CloudFormation is IaC.