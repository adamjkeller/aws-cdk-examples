from aws_cdk import cdk
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancing as elb,
)


class LoadBalancerStack(cdk.Stack):
    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        vpc = ec2.VpcNetwork(self, "VPC")

        asg = autoscaling.AutoScalingGroup(
            self,
            "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceTypePair(
                ec2.InstanceClass.Burstable2, ec2.InstanceSize.Micro
            ),
            machine_image=ec2.AmazonLinuxImage(),
        )

        lb = elb.LoadBalancer(
            self, "LB", vpc=vpc, internet_facing=True, health_check={"port": 80}
        )
        lb.add_target(asg)

        listener = lb.add_listener(external_port=80)
        listener.connections.allow_default_port_from_any_ipv4("Open to the world")


app = cdk.App()
LoadBalancerStack(app, "LoadBalancerStack")
app.run()
