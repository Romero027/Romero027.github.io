# Summary of "Towards Federated Learning at Scale: System Design"
Xiangfeng Zhu(zxfeng), Jiachen Liu(amberljc), Chris Chen(zhezheng)

## Problem and Motivation

The goal is to build a system that can train a deep neural network on data stored on the phone which will never leave the device. The weights are combine in the cloud with Federated Averaging, constructing a global model which is pushed back to the phone for inference.


## Solution Overview

### Device-server protocol

Each round of the protocol contains three phases. 
**Selection**: The server(i.e. the coordinator in the server) picks a subset of available devices to work on a specific FL task[1]. 
**Configuration**: The server sends the FL plan(execution plan) and the FL checkpoint(i.e. a serialized state of a Tensorflow session) with the global model to each of the chosen devices. When receiving a FL task, the FL runtime will be responsible for performing local training.
**Reporting**: The server waits for the participating devices to report updates. The round is considered successful if enough devices report in time. (The update to the model is often sent to the server using encrypted communication.)
As an analogy, we can interpret the FL server as the reducer, and FL devices as mappers. 

In FDS, data is logically stored in **blobs**, which is a byte sequence named with a 128-bit GUID. Reads from and writes to a blob are done in units called **tracts**. Empirically, they found that 8MB makes random and sequential access achieves nearly the same throughput. Every disk is managed by a process called a **tract server** that services read and write requests that arrive over the network from clients. FDS uses a **metadata server** to store the location of tracts.

<p align="center">
    <img src="http://xzhu27.me/fds/architecture.png" alt="image"/>
</p>

#### Metadata Management

<p align="center">
    <img src="http://xzhu27.me/fds/table.png" alt="image"/>
</p>

FDS uses a metadata server to store the information about data placement, but it only stores the tract locator table(TLT). Each TLT entry, with k-way replication, contains k tractservers. The client applies the following function to get entries in TLT, called **tract locator**. Once clients find the proper tractserver address in the TLT, they send read and write requests containing the blob GUID, tract number. 

<p align="center">
    <img src="http://xzhu27.me/fds/hash.png" alt="image"/>
</p>

Different from inode in UNIX, the TLT does not contain complete information about the location of individual tracts in the system.(We will compare TLT against DHT and NameNode in Hadoop later). The metadata about each blob is stored in its special metadata tract("tract - 1"). 

Note that TLT changes only in response to cluster reconfiguration or failures and is not modified by tract reads and writes. Thus, TLT entries can be cache by clients for a long time. 

#### Dynamic Work Allocation

In FDS, since storage and compute are no longer colocated, the assignment of work to worker can be done dynamically, at fine granularity, during task execution. The best practice for FDS applications is to centrally (or, at large scale, hierarchically) give small units of work to each worker as it nears completion of its previous unit. Since,  in BSP, all tasks in the previous stage have to finish before the current stages begin, such design eliminates stragglers. 

#### Replication

FDS uses replication both for availability and fault tolerance. When an application writes a tract, the client library finds the appropriate row of the TLT and sends write to every tractserver it contains. Reads select a single tractserver at random. When a tract server receives create, extend or delete blob requests(i.e. operations which modify the metadata tract), it executes a two-phase commit with the other replicas. 

#### Recovery

Each TLT entry also has a version number, canonically assigned by the metadata server. When the metadata server detects a tractserver timeout, it declares the tractserver dead. Then, it invalidates the current TLT by incrementing the version number of each row in which the failed tractserver appears and picks random tractservers to fill in the empty spaces. Table versioning prevents a tractserver that failed and then returned. The paper provides more details and examples about the recovery protocol. 


## Compare to HDFS/GFS

Hadoop and GFS both have a centralized master that keeps all metadata in memory. Files and directories are represented on the master/NameNode by inodes, which record attributes like permissions, modification and access times, namespace and disk space quotas. Although such design provides one-hop access to the data and can recover from failure promptly, as the contents of the store grow, the master becomes a centralized scaling and performance bottleneck. 
In contrast, the tract locator table's size is determined by the number of machines in a cluster, rather than the size of its content.

(Figure 1 credits to Mosharaf Chowdhury and Figure 2,3 credit to Alex Rasmussen)
