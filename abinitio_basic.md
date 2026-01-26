Why Ab Initio Was (and Still Is) Years Ahead of Modern ETL ...Yes, Ab Initio is a powerful enterprise platform widely recognized and used as an ETL (Extract, Transform, Load) tool, but it's much more, serving as a comprehensive data integration, processing, and management solution for large-scale, complex data environments, featuring parallel processing, metadata management, and robust automation.  
Key Aspects of Ab Initio as an ETL Tool:
Data Integration: Excels at extracting data from diverse sources, transforming it, and loading it into target systems like data warehouses or lakes. 
Graphical Development: Uses a visual, drag-and-drop interface (GDE - Graphical Development Environment) to design data flows (graphs). 
Parallel Processing: Built for massive parallel processing, enabling efficient handling of large datasets. 
Comprehensive Platform: Beyond basic ETL, it includes features for data quality, metadata management, data profiling, and scheduling, making it a full data processing environment. 
Scalability & Performance: Known for its ability to scale and manage complex data pipelines effectively, often outperforming simpler tools. 
In essence, while it perfectly fits the definition and function of an ETL tool, Ab Initio offers advanced capabilities that position it as a complete data platform, not just a basic ETL utility.










Context and trajectory

Enterprise ETL platforms such as Ab Initio occupy a transitional space in modern data architectures. Historically they provided high‑performance, GUI‑driven, batch-oriented data integration with strong governance and operational controls. Today they face pressures from cloud-native data platforms, open-source tooling, streaming requirements, and shifting economics. The future is not binary (dead vs. dominant); it’s a mix of consolidation, specialization, and evolutionary adaptation.

Key forces shaping the future

Cloud migration and SaaS: Organizations are moving data workloads to cloud-managed services (Snowflake, BigQuery, Redshift, Databricks, cloud ETL SaaS). That reduces demand for heavy on‑prem ETL footprints unless vendors provide cloud‑native deployments or managed offerings.
Streaming and real‑time needs: Increasing demand for low-latency ingestion and event-driven pipelines favors streaming-first frameworks (Kafka, Flink, ksqlDB) or ETL tools that integrate realtime processing alongside batch.
Modern data stack and ELT pattern: The ELT approach—load raw data into a central cloud warehouse/lakehouse, then transform with SQL/compute in place—erodes some classical ETL roles. Tools that adapt to orchestrate ELT and provide metadata/observability retain relevance.
Open source and developer-first tools: Airflow, dbt, Spark, and Flink have changed buyer expectations: modularity, code-centric workflows, community ecosystems, and lower licensing costs.
Governance, observability and data contracts: As scale and regulation grow, enterprises still need lineage, quality checks, auditing, and operational robustness—areas where mature ETL platforms excel.
Total cost of ownership and skills: Licensing, specialized skill requirements, and vendor lock‑in matter. Organizations balance platform capabilities against hiring and operational costs.
Likely scenarios for vendors like Ab Initio

Evolution toward hybrid/cloud-native offerings: Successful legacy vendors will offer managed/cloud-deployable versions, containerized runtimes, and connectors to cloud storage/warehouses and streaming platforms. Partial lift-and-shift for existing customers and new cloud-native modules for greenfield projects.
Focused differentiation on enterprise features: Strengthening areas that cloud-native tools struggle with—high-throughput batch at scale, complex PII transformation with strict governance, guaranteed exactly-once semantics for mission-critical flows, and built-in operational tooling (visual debuggers, SLA monitors).
Interoperability and orchestration play: Acting as a control plane that integrates streaming sources, cloud warehouses, dbt transformations, and orchestration engines—exposing APIs, metadata services, and lineage to coexist with the modern stack.
Vertical specialization: Targeting industries with heavy compliance, latency, or legacy complexity (finance, telecoms, utilities, government) where proven deterministic processing and support are valued.
Gradual market contraction for purely on‑prem, monolithic platforms: New projects increasingly prefer modular or cloud alternatives. Legacy deployments will persist but shrink as workloads modernize or are replaced.
What buyers and architects should consider now

Inventory and classify workloads: Separate mission‑critical, high‑performance batch jobs and complex legacy transformations (candidates to keep on platforms like Ab Initio) from greenfield analytics, exploratory, and ELT workloads (better served by cloud/data‑stack tools).
Adopt a hybrid integration strategy: Use best‑of‑breed: cloud ELT + dbt for analytics, streaming platforms for real‑time, and enterprise ETL where deterministic, governed transformations are required. Ensure metadata, lineage, and orchestration are centralized.
Evaluate migration paths pragmatically: Rewriting every pipeline is expensive and risky. Prioritize based on business impact, cost, and technical feasibility. Consider wrapping existing ETL as a service, reusing tested components, or incremental replatforming.
Demand API/connector openness and metadata export: If keeping a legacy ETL product, require exportable lineage, catalog integration, and automation hooks to avoid future lock‑in.
Build skills and governance: Invest in platform‑agnostic skills (SQL, streaming concepts, data modelling, orchestration) and in governance practices that make tooling interchangeable over time.
Practical short‑term bets (12–36 months)

Expect continued use of Ab Initio and similar tools in regulated, high-throughput environments, with a steady but slow shift toward hybrid deployments.
New analytics and product development projects will prefer cloud-native ELT/ELT + dbt + orchestration stacks.
Vendors that rapidly provide cloud/managed options, open metadata, and streaming capabilities will retain or grow enterprise accounts.
Bottom line

Ab Initio‑style ETL tools will not disappear overnight; they will persist where their deterministic performance, operational controls, and governance are essential. Their long‑term relevance depends on how quickly they adapt to cloud, streaming, open metadata, and orchestration paradigms. Organizations should adopt a pragmatic hybrid strategy: preserve and modernize critical legacy pipelines while building new capabilities on modular, cloud‑native stacks that lower cost and accelerate analytics.



This question has been asked for many years now but if you see, Ab Initio is still going very strong. If Ab Initio would have just been an ETL tool, it might have lost the race because of its cost and strict content sharing principle. But Ab Initio is much more than just an ETL tool. With EME (code storage and versioning), Conduct IT (wrapping & dependency handling), Operational Console (scheduling), Data Profiler (data quality), Metadata hub (metadata management), BRE + ACE (Generic code with minimal developer need for code enhancements), Continuous flows and web service features (real time services) and many more tools & features, it is a full-fledged, data and metadata management tool.
Before I digress any further, what I mean to say is that Ab Initio is being used heavily & will continued to be used by companies because of the power of the tool and the myriad other benefits it brings along. All its tools are tightly coupled and are very easy to use which is another plus point. And Ab Initio is keeping up with the technological advancements like Big Data and Hadoop by providing fair interfacing mechanisms and is constantly improving.
Another important thing that I see today is that the number of people with Ab Initio as a skill have increased quite a lot from past which is another good sign.
Being said that, companies who are looking for a single-stop solution and are not short on cash will more than often go for Ab Initio. It will and should continue to flourish in coming times.



Ab Initio has evolved well with the technology. It has kept its competitive edge by introducing new add-on's , parser's , connectors and components that can read and write files in multiple formats.

Its just not an ETL as Shashi rightly pointed out , it is one stop shop for all your data transfer and processing needs. With tools like Express>IT , BRE , data profiler etc. it has become a complete data processing solution for any business.

Only challenge is the price card but its worth it. If you don't want 10 tools with 10 management consoles and would like to have 1 tool which can do everything for you and which is faster, this is what you are looking for.



AB Initio is the ruling ETL Tool nowadays and it is going be used for the next coming years widely. Ab Initio a Business Intelligence platform comprised of six data processing products; Co-Operating System, The Component Library, Graphical Development Environment, Enterprise Meta-Environment, Data profiler, and Conduct-It. Itis a powerful GUI-based parallel processing tool for ETL data management and analysis. modern-day technologies to solve business problems.Ab Initio Software is a widely used Business Intelligence Data processing platform. It is used to build a vast majority of business applications- from operational systems, distributed application integration, and complex event processing to data warehousing and quality management systems. ern-day tech


I once got virtually slapped for calling Ab Initio a tool and rightly so! Rather than thinking of it as an ETL gimmick, consider it a massively parralel, linearly scaling data integration platform, backed by the world's smartest developers and businesses strategists. As such, the question to really ask would be ‘what is the future role of data integration and business intelligence’? For whatever your answer to that question, my answer to the second part would be that Ab Initio has been riding on top of that wave for very many years now.


The future is not to bright for most of the mainstream ETL tools except Ab-Initio as ELT is the future of data warehousing. Light weight tools like Talend are expected to do much better. Ab-Initio is an exception because it was denied for several firms in the past and now with the major organisations moving out of Ab-Initio will force them to provide solutions for smaller companies. This will keep it alive longer than most of the other tools like datastage or SSIS.

I have used ABINITIO, Informatica, SSIS and talend in my professional journey while working for major retail and finance corporations. This is the basis of my reply.


Here are some things to think about regarding the future of ETL tools like Ab Initio and Skyvia:

Ab Initio: An effective ETL tool with scalability, parallel processing, and data integration capabilities is called Ab Initio. The key to its future is to keep up with emerging technological trends like big data, cloud computing, and real-time data processing. Ab Initio may prioritize developing these features and strengthening its integration with cutting-edge data platforms.

However, Skyvia is an integration platform as a service (iPaaS) that offers data integration and ETL capabilities. Its future is in providing a solution to data integration that is user-friendly and cloud-based. With capabilities like AI-driven automation, self-service data preparation, and closer connectivity with cloud-based data platforms and services, Skyvia may keep improving its platform.

contemporary Data Architectures: The move toward contemporary data architectures will influence the development of ETL tools, such as Ab Initio and Skyvia. This includes implementing big data technology, real-time streaming data processing, and cloud-based data platforms. These architectures will require adaptation and support from ETL tools in order to provide seamless integration, scalability, and adaptability.

===




Here are some things to think about regarding the future of ETL tools like Ab Initio and Skyvia:

Ab Initio: An effective ETL tool with scalability, parallel processing, and data integration capabilities is called Ab Initio. The key to its future is to keep up with emerging technological trends like big data, cloud computing, and real-time data processing. Ab Initio may prioritize developing these features and strengthening its integration with cutting-edge data platforms.

However, Skyvia is an integration platform as a service (iPaaS) that offers data integration and ETL capabilities. Its future is in providing a solution to data integration that is user-friendly and cloud-based. With capabilities like AI-driven automation, self-service data preparation, and closer connectivity with cloud-based data platforms and services, Skyvia may keep improving its platform.

contemporary Data Architectures: The move toward contemporary data architectures will influence the development of ETL tools, such as Ab Initio and Skyvia. This includes implementing big data technology, real-time streaming data processing, and cloud-based data platforms. These architectures will require adaptation and support from ETL tools in order to provide seamless integration, scalability, and adaptability.


I guess Ab Initio will continue to be one of the market leaders. Even back in 2008 when I used Ab Initio it had features that no other ETL tools had back then and some of the ETL tools don’t even have it even now. As the size of the data to be processed is getting larger and larger Ab Initio will continue to be one of the most preferred ETL Tool.



Based on my experience ETL tools will become more of subset of the applications rather than doing the major transformations. Importance will be reduced and Hadoop based systems will be used more.

ETL tools will be used the as a complimentary technology along with HDFS or data lakes.

Applications which doesn't use non structured data will keep living on ETL tools but organizations are moving toward the storing the non structured data into Data lakes or Hadoop based file systems which will eventually reduce the use of ETL


Originally Answered: What is the future of ETL tools like Ab Initio in 2019?
Unfortunately it will just be used by heavy customers who are ready to pay. Its expensive but a powerful tool. I guess it will just stay with Banks and Insurance companies (mostly). Hard to see it being used elsewhere/other domains.


 · 

Ab Initio has many features, BRE..ACE etc How many companies are fully utilising? No console, flawed Ops console. Ability to process real time. How many companies are using it for online transaction processing? It's glorified ETL and NOT a form of application development as many tout it to be.

Profile photo for Viswajit Nayak
Viswajit Nayak
experienced professional
 · 

Looks like it is not so bright now :P

Profile photo for Anonymous
Anonymous
8y
Related
AB Initio ETL has no future any more. What is the transition career path for an Ab Initio ETL developer to other technologies and products based on the current and future market trend?
What makes you think that Ab Initio has no future? Anyway your question sounds like you have already made a judgement.

Just because you know that 5–6 companies that you heard about are moving away from Ab Initio? This has always been happening, ever since Ab Initio came into the market. Not only Ab Initio, companies have moved away from SSIS, Informatica and adopted other technologies time and again.

Do not worry, Ab Initio is pretty versatile, and Ab Initio corp keeps on adding new features to make it compatible with newer technologies and frameworks like big data etc. and Ab Initio has always

Profile photo for Swapnil Agnihotri
Swapnil Agnihotri
Software architectAuthor has 189 answers and 596.8K answer views
 · 
9y
Related
Who are the clients of ETL tool - Ab Initio corporation? Will Ab Initio be the future of ETL?
Well ABINITIO is there is almost fortune 50 firms. ABINITIO chooses the companies where it can be used and is very expensive (comparatively). This is the prime reason for it to be not widely used. Having said that, now the major projects using ABINITIO are moving to other tools. This would force ABINITIO company to open up to mid-level corporations and reductions in cost in the future.

I would recommend not to stick to ABINITIO as for primary skill for the long term. The same is true for any other tool for sure… learn the concepts of ETL and apply it on divergent tools like Informatica, data st

Profile photo for Debayan Bhattacharjya
Debayan Bhattacharjya
9y
Related
Do I have any future in ETL tool?
Yes Absolutely.
Business Intelligence is one of the most trending topics in IT sector and its pretty cool as well..

And it is a vast concept and out of it ETL has been a very core and important aspect.
If you are working with ETL , not only you will learn respective tool but at the same time you will have the following things
a)Have a very good analyzing power as you need to bring different sets of data across platforms and put it into a meaningful format .
b)You will understand the internal data modeling for the project.
c)You need to do several processes like data clensing,profiling etc whic

Profile photo for John Rainey
John Rainey
Plays with Computers and Equations.Author has 2K answers and 4.7M answer views
 · 
8y
Related
How can we compare the AB Initio and Pentaho ETL tools?
If my experience with Ab Initio ETL tool is any indication, then you will find little information publicly. Ab Initio doesn't really actively market their products. At least nothing like Informatica or Data Stage.

I can tell you that An Initio ETL will process huge volumes of data very efficiently and quickly. I have been using An Initio since 1998 and it is an utterly amazing ETL tool. There is none better on the market that I have seen. I have seen POC's where Ab Initio would complete a huge data problem and hours later the comparable tools would still be processing. Ab Initio also has a nice

Profile photo for Swapnil Agnihotri
Swapnil Agnihotri
Works at Citigroup (company)Author has 189 answers and 596.8K answer views
 · 
8y
Related
Who will lead ETL in the future, Ab Initio or Informatica?
Neither, they are both infra hungry. Future seems brighter for light weight tools

Profile photo for Soham Dutta
Soham Dutta
Lives in San Francisco Bay Area (2016–present)
 · 
5y
Related
What are the best current ETL tools?
The ETL tools marketplace is quite cluttered currently with tools supporting only the data pipelines to tools supporting the end to end data management. However, I would like to recommend tools that follow the modern architecture of ELT rather than ETL. Some of the ELT tools are as follows.

Fivetran: Fivetran is a totally regulated data pipeline with a web interface that consolidates data from SaaS organizations and databases into a single data stockroom. It gives direct compromise and sends data over a direct secure affiliation using a cutting edge saving layer. This saving layer helps with mo
Profile photo for Eli Mshomi
Eli Mshomi
Studied at Africa
 · 
9y
Related
Do I have any future in ETL tool?
Yes you have a future in ETL tools…depending on what Tool ….and how deep you want to go

Informatica - Its highly used ETL tool you can't go wrong with it but after knowing the basics ..then concentrate on the following. ILM - Informatica Lifecycle Management , IDQ - Data Quality and data Cleansing , Informatica XML and WebServices …, there a lot of opportunities …its used by bigger organizations
SSIS - SQL Server Integration Services - Lot of future there especially if you want to be entrepreneur and do your own projects..It comes with Sql Server and part of Visual Studio ….its affordable for mo
Profile photo for Soham Dutta
Soham Dutta
Lives in San Francisco Bay Area (2016–present)
 · 
5y
Related
Which ETL tool has a promising future?
There are a few ETL tools available in the market which are doing good currently and looks to have a promising feature.

Matillion: Matillion's ETL apparatus is, as indicated by its engineers, reason worked for cloud data warehouses, so it could be an especially solid decision for clients who are particularly keen on stacking data into Amazon Redshift, Google BigQuery or Snowflake. With more than 70 local data source combinations, just as a discretionary no-code graphical interface, Matillion makes stacking your data into your warehouse of decision basic and direct. It likewise mechanizes the da

Profile photo for Vincent Jiang
Vincent Jiang
Founder and CEO of AchoAuthor has 314 answers and 1.4M answer views
 · 
5y
Related
Which ETL tools do you prefer and why?
There’re many ETL tools. It really depends on what you focus on. These tools each does something differently with pros and cons.

Things to consider when choosing an ETL tool are

1. integrations

What type of data are you connect to? If it’s a third-party app, it actually works a bit differently than setting up a connection with a database. If you’re connecting a real time database, performance would matter a lot.

2. performance and scalability

The faster the better of course! However, there can be many back-end issues with speed that can cause data loss.

3. level of automation

This is more of a person

Profile photo for Kunal Ghosh
Kunal Ghosh
Proven expertise in DI / DE / DW / Cloud / Hadoop / Spark
 · 
8y
Related
What are the best current ETL tools?
I do not know how much data are you talking about.

Here is a good answer Which is the best ETL tool to learn and which has good job opportunities?

I would recommend tools which are widely used and have sustained reputation and known to working.

I personally developed pipelines using.

Ab Initio - This is very expensive but they are the best you can get. To me there is them and the rest. Some time back all major Credit Cards, Banks and Insurance companies were using them.
The rest would include

Enterprise Cloud Data Management (Informatica)
Talend Real-Time Open Source Big Data Integration Software -Th
Profile photo for Shubhnoor Gill
Shubhnoor Gill
Studied B.E. Computer Science Engineering with Specialization in Artificial Intelligence and Machine Learning. at Chandigarh University (Graduated 2022)
 · 
4y
Related
Which ETL tool has a promising future?
There are many ETL Tools in the market. Some of them are quite popular and some not. But all have their pros and cons. Some of the ETL tools which have a promising future are:

Hevo Data
Stitch
AWS Glue
Talend
And many more…

But let me discuss one of the promising tools out of these on the basis of Business reviews - Hevo Data.

Hevo Data is a No-Code Data Pipeline, that provides an interactive interface. It supports 100+ Data Integrators and helps perform ETL processes in a secure, real-time, and hassle-free manner. The best part that businesses love about Hevo is its detailed documentation and live s

Profile photo for Simcha Lazarus
Simcha Lazarus
Community Manager at Lightricks (2018–present)Author has 123 answers and 245.1K answer views

How can we compare the AB Initio and Pentaho ETL tools?
We don’t yet have any reviews for AB Initio over at IT Central Station, but you’re welcome to visit our site and see what other tools are often compared to Pentaho.

Here are some comparison pages that you might find helpful:

Pentaho Data Integration vs WhereScape RED
Pentaho Data Integration vs IBM InfoSphere DataStage
Pentaho Data Integration vs webMethods
You can also visit the Data Integration page to see what other solutions are popular with IT Central users.

Profile photo for Shubhnoor Gill
Shubhnoor Gill
Studied B.E. Computer Science Engineering with Specialization in Artificial Intelligence and Machine Learning. at Chandigarh University (Graduated 2022)
 · 
4y
Related
Which tool is the latest one in ETL?
Some of the types of ETL (Extract Transform Load) Tools available in the market are:

Cloud ETL Tools: AWS Glue, Hevo Data, Google Cloud Dataflow, Stitch
Enterprise Software ETL Tools: Informatica PowerCenter, IBM InfoSphere DataStage, Microsoft SQL Server Integration Services
Open Source ETL Tools: Pentaho Data Integration, Hadoop, Talend Open Studio
Among them, Hevo Data is the latest popular ETL tool in the market. Hevo Data provides its users with a simple and interactive platform for integrating data for analysis. It is a no-code data pipeline that can help you combine data from multiple sourc

Profile photo for Mohankrishna Bellamkonda
Mohankrishna Bellamkonda
ITA at Tata Consultancy Services (company) (2011–present)
 · 
8y
Related
Why do we need ETL tools?
Consider you are currently working on oracle DB. What ever the logic we frame using ETL can be done using SQL / PLSQL itself. Then why do we need ETL tools ?

connectivity with multiple DBs : If you want to migrate from oracle to some other DB , you have to rewrite your complete PLSQL code according to New DB syntaxes , which requires expert in that DB area and takes lot of time and effort . ETL tools makes this simple. We just have to configure the connection as per New DB.
Graphical User Interface : Most of the ETL tools have Graphical User Interface which will help to code the complex logic in
Profile photo for Naveen S
Naveen S
Lives in Bengaluru, Karnataka, India
 · 
8y
Related
Who will lead ETL in the future, Ab Initio or Informatica?
Now a days all the companies (small/medium) is going for the freeware tools (like TALEND), which are licensed free and opts all the features of the current Big ETL tools. Informatica is completely moving to cloud and bigdata edition and as for abinitio goes I'm not seeing that much openings now a days

Profile photo for Jenny Kristal
Jenny Kristal
Former Data Scientist
 · 
2y
Related
Which ETL tools do you prefer and why?
The ones I prefer are the ETL tools that:

are simple and easy to use
meets my requirements
will rarely make me call support because the documentation and/o community are reliable. Or a simple Google or Bing for the problem at hand solves the problem quickly.
That said, I used Microsoft SSIS, Talend Open Studio, and Skyvia. These 3 met the above. If there are requirements that these 3 may not meet, I may consider others. But usually they cover almost all data integration use cases.

Profile photo for Anoop Kumar VK
Anoop Kumar VK
15+ y in BI | Business Intelligence Demystified book AuthorAuthor has 343 answers and 729.8K answer views
 · 
Updated 4y
Related
What is the best ETL tool to work with, Informatica or AB Initio? What are the job perspectives for them in India?
Both the ETL tools (Informatica and Ab Initio) are very good tools and are leading tools in its category. Based on a survey conducted end of 2016, Informatica was considered as better tool from a developer’s perspective. Both tools have good job prospects.

Original question: What is the best ETL tool to work with, Informatica or AB Initio? What are the job perspectives for them in India?

Profile photo for Rajnish Sahay
Rajnish Sahay
Works at IBM (company)Author has 107 answers and 186.3K answer views
 · 
6y
Related
ETL by code vs ETL tool, which one do you prefer and why?
Back in the olden days (late 90’s) ETL tool did not exist. We used to code using PL/SQl stored procedures, SQL loader and SQL scripts to mimic the ETL functionality.

Then in 2001 , there was an arrival for ETL tools . I remember when I used to work for Perot Systems in USA Boston , representatives from Ascential used to visit frequently to demo Datastage ETL tool.


But the automated tool still took few years to pick up. 2006 onwards there was a good demand of GUI based ETL tools and many tools like Datastage , Ab Initio , Informatica etc picked up.


Since it has been almost 15 years with ETL tools

Profile photo for Avinash Gupta
Avinash Gupta
MD at FEG IndiaAuthor has 324 answers and 1.9M answer views
 · 
6y
Related
Which ETL tool has a promising future?
None, the ETL tools have to emerge which are completely serverless and based on cloud.

They should have addons to capture change fron on premise and ingest into cloud seamlessly.

They should process more data on the databases rather than on their own servers.

Provide integration within cloud products and on premise databases.

There are few which are looking good like Matillion ETL for Amazon Redshift | ETL for Redshift

It is available for both AWS and GCP.

Profile photo for Anonymous
Anonymous
Updated 9y
Related
Which companies in the USA use Ab Initio ETL tool?
Some of the companies that I know use Ab Initio:

American Express
Premier
Citi Bank
JP Morgan Chase
TransUnion
All State
Time Warner Cable
Home Depot
Capital One
SunTrust Banks
Wells Fargo
The following seem to have discontinued using Ab Initio:

First Data Corporation
Bank of America
Adding these as per comments :


 · 

What is the future of the tool based ETL (Extract, Transform, Load)?
The future of ETL tools is not completely dull. There will still be use cases where a ETL tool will still find place like in case of Enterprise BI development. There are also cloud based ETL programs which provides ETL functionality. Wherever multiple RDBMS systems are involved, ETL tools will have role to play.

Profile photo for Martin O'Shea
Martin O'Shea
Lives in LondonAuthor has 2.2K answers and 4M answer views

What is the future of the tool based ETL (Extract, Transform, Load)?
I have no crystal ball that I can read to tell you the future of tool-based ETL. The best I can I suggest is that you do a keyword search of Google or Bing and read links like:


 · 

What is the future of the tool based ETL (Extract, Transform, Load)?
It will likely exist in some form… some may call it data wrangling, data pipeline or something else completely. I doubt it will go away. We are human and know how to make mess of data… ETL provides an easy way to load those data-mess into database.

Profile photo for Mohammed Zulfiquar
Mohammed Zulfiquar
Datawarehouse/BI professional. US Citizen
 · 

AB Initio ETL has no future any more. What is the transition career path for an Ab Initio ETL developer to other technologies and products based on the current and future market trend?
AWS ETL, Azure Data Lake or Google Cloud Big Query, with Big Data technologies like Hive, Pig, HBASE etc. Splunk, Scala, Kafka.


How do I practice on Ab Initio Tool for free?
You can't. Ab initio is a commercial tool. You need to get license to use. You can use this tool only if you are working on a service based project. Companies like Citi, Visa inc. , Barclays, etc use Ab initio tool extensively. If you are in any service based companies working with these kind of clients try to get into those projects. Best of luck!!!
