# k8s from scratch notes

## Worker Node

### Containerd (container runtime)

Containerd is a high-level container runtime that serves as the foundation for container management on Kubernetes worker nodes. Containerd organizes k8s pods in their own namespace `k8s.io`.

- Industry standard: containerd is a CNCF-maintained, industry-standard container runtime that originated from Docker and powers container execution in Kubernetes clusters
- Modular architecture: containerd orchestrates container operations while delegating specific tasks to specialized components: OCI runtimes (like runc) handle process execution and CNI plugins manage networking
- Essential services: Provides container lifecycle management, image management, storage coordination, and network interface setup for Pods
Management tools: Use ctr for low-level debugging and nerdctl for Docker-like commands when working directly with containerd

#### runc (low-level oci runtime)

The OCI Runtime Specification standardizes how containers should be created, started, and managed at the low level, abstracting away platform-specific isolation details. This allows high-level runtimes like containerd to work with any OCI-compliant (aka. low-level) runtime without knowing the implementation details.

#### CNI (Container Network Interface)

CNI is a specification and set of libraries for configuring network interfaces in Linux containers. It provides a standardized way for container runtimes to set up container networking, including creating network namespaces, configuring IP addresses, and establishing connectivity between containers and the host system.

### Kubelet (k8s node agent) and kubeletctl

kubelet is the primary node agent that runs on every worker node in a Kubernetes cluster. As one of the core components that makes Kubernetes work, it acts as the bridge between the Kubernetes control plane and the container runtime on each node.

- Control plane bridge: kubelet acts as the essential link between the Kubernetes control plane and the container runtime, translating API server instructions into container operations
- Reconciliation loop: Continuously watches for Pod specifications, compares desired vs actual state, and takes corrective actions to maintain cluster consistency
- CRI delegation: Doesn't run containers directly but communicates with container runtimes like containerd through the Container Runtime Interface (CRI)
- Static Pods: Enables running critical cluster components directly on nodes before the control plane becomes available, with automatic restart capabilities
- API endpoint: Provides an HTTP interface on port 10250 for log access, metrics, and container execution, essential for cluster operations

kubeletctl is a command-line tool that provides direct access to the kubelet API. It's useful for debugging and inspecting kubelet instances, querying pod information, retrieving logs, and exploring kubelet's internal state without requiring a full Kubernetes cluster setup.

#### CRI (Container Runtime Interface) and crictl

The Container Runtime Interface (CRI) is a gRPC API that defines a standard interface for kubelet to interact with container runtimes. It enables kubelet to work with any CRI-compatible container runtime, without runtime-specific code compiled into kubelet.

The CRI API consists of two main services:
- RuntimeService: Manages pod sandboxes and containers (create, start, stop, remove, etc.)
- ImageService: Manages container images (pull, list, remove, etc.)

crictl is the official CLI tool for interacting with CRI-compatible container runtimes. It's designed to help debug and inspect containers and images managed by kubelet.

---

## Control Plane

### etcd

### kube-apiserver

### kube-scheduler

### kube-controller-manager
