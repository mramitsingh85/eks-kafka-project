resource "aws_msk_cluster" "kafka" {
  cluster_name           = "msk-kafka"
  kafka_version          = "3.6.0"
  number_of_broker_nodes = 2

  broker_node_group_info {
    instance_type   = "kafka.t3.small"
    client_subnets  = module.vpc.private_subnets
    security_groups = [module.vpc.default_security_group_id]
  }
}