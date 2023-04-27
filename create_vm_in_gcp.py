# Please run "pip install google-api-python-client" before executing
import googleapiclient.discovery


compute = googleapiclient.discovery.build('compute', 'v1')
true = True
false = False


# [list_instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


# [Create_VM]
def create_instance(compute, project, zone, name, bucket):
    # Get the latest Debian image.
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-11').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


before_creating = list_instances(compute, 'project_name', 'zone')
print("Before Creating VM: {}".format(before_creating))

create_vm_response = create_instance(compute, 'project_name', 'zone', 'vm_name', 'pybucket')
print("Create VM response: {}".format(create_vm_response))

after_creating = list_instances(compute, 'project_name', 'zone')
print("After Creating VM: {}".format(after_creating))
