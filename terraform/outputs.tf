output "cluster_name" {
  value = module.eks.cluster_name
}

output "msk_bootstrap_servers" {
  value = aws_msk_cluster.kafka.bootstrap_brokers
}