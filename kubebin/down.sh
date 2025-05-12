for item in kubeadm kubectl kubelet
do
wget https://dl.k8s.io/v1.31.4/bin/linux/amd64/$item
done
