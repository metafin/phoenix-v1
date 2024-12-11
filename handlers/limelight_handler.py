# limelight_handler.py
import limelight
import limelightresults
import time

class LimelightHandler:
    def __init__(self, debug=True):
        self.discovered_limelights = limelight.discover_limelights(debug=debug)
        self.limelight_instance = None

        if self.discovered_limelights:
            print("Limelight init: Limelight found and active", self.discovered_limelights)
            limelight_address = self.discovered_limelights[0]
            self.limelight_instance = limelight.Limelight(limelight_address)
            self.limelight_instance.pipeline_switch(0)  # Switch to AprilTag detection pipeline
            self.limelight_instance.enable_websocket()
        else:
            print("Limelight init: ERROR: No Limelights found")

    def read_results(self):
        print("Limelight read_results: starting")
        if self.limelight_instance:
            print("Limelight read_results: there is an instance")
            result = self.limelight_instance.get_latest_results()
            print("Limelight read_results: result:",result)
            parsed_result = limelightresults.parse_results(result)

            if parsed_result is not None:
                print(
                    "valid targets: ", parsed_result.validity, ", pipelineIndex: ", parsed_result.pipeline_id,
                    ", Targeting Latency: ", parsed_result.targeting_latency
                )
                for tag in parsed_result.fiducialResults:
                    print(f"Limelight read_results: AprilTag ID: {tag.fiducial_id}, Robot Pose: {tag.robot_pose_target_space}")

    def cleanup(self):
        if self.limelight_instance:
            self.limelight_instance.disable_websocket()
