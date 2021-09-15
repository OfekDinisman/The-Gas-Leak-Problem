



class TestModel:
    def __init__(self, scheduled_tasks, emergencies, resources, assigned_resources, COMPLIANCE_RATE, DELAY_TIME, RESOURCE_SPEED) -> None:
        self.scheduled_tasks = scheduled_tasks
        self.emergencies = emergencies
        self.resources = resources
        self.assigned_resources = assigned_resources
        self.COMPLIANCE_RATE = COMPLIANCE_RATE
        self.DELAY_TIME = DELAY_TIME
        self.RESOURCE_SPEED = RESOURCE_SPEED

    def getAppointmentsResource(self, assignment_id):
        return self.assigned_resources[assignment_id] # return resource_id

    def run(self):
        pass


