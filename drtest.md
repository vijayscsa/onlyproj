Seeing `Kind: ReplicaSet` under your pod's owner references confirms that your pod is managed by a higher-level controller (typically a Deployment, which creates and manages that ReplicaSet).

Because a ReplicaSet constantly monitors your pods against its desired state, any unexpected pod termination triggers an automatic replacement. Here is how you can safely test failover and autoscaling for this critical component.

---

### Step 1: Identify the Parent Deployment

Since the ReplicaSet is usually owned by a Deployment, finding the Deployment name lets you control scaling and autoscaling properly. Run this command to check the owner of your ReplicaSet:

```bash
kubectl get replicaset <replicaset-name> -n <your-namespace> -o jsonpath='{.metadata.ownerReferences[*].name}'

```

* **Expected Output:** The name of your parent **Deployment** (e.g., `my-critical-app-deployment`).

---

### Step 2: Test Pod Failover (Self-Healing)

To verify that your cluster automatically recreates the critical pod when it crashes or fails:

1. Open a terminal window and watch your pods in real-time:
```bash
kubectl get pods -n <your-namespace> -w

```


2. In a separate window, delete the running pod to simulate an abrupt failure:
```bash
kubectl delete pod <your-pod-name> -n <your-namespace>

```


3. **Verification:** Look back at your watching terminal. You will instantly see the old pod terminate (`Terminating`), and the ReplicaSet will immediately spin up a brand-new replacement pod (`Running`).

---

### Step 3: Test Autoscaling

If your team's goal is to test **Horizontal Pod Autoscaling (HPA)**, you need to verify whether an HPA rule is already active or test manual scaling:

1. Check if an HPA is linked to your deployment:
```bash
kubectl get hpa -n <your-namespace>

```


2. If an HPA exists, you can test autoscaling by generating artificial CPU or memory load inside the app, or temporarily modify the scaling limits.
3. Alternatively, you can test multi-replica availability manually by scaling the deployment:
```bash
kubectl scale deployment <deployment-name> --replicas=3 -n <your-namespace>

```


4. **Verification:** Run `kubectl get pods -n <your-namespace>` to confirm that all three replica pods start successfully and distribute your workload.

---
