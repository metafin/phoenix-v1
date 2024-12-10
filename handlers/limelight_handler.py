# limelight_handler.py
import limelight
import limelightresults
import time

class LimelightHandler:
    def __init__(self, debug=False):
        self.discovered_limelights = limelight.discover_limelights(debug=debug)
        self.limelight_instance = None

        if self.discovered_limelights:
            print("Found an April Tag")
            limelight_address = self.discovered_limelights[0]
            self.limelight_instance = limelight.Limelight(limelight_address)
            self.limelight_instance.pipeline_switch(0)  # Switch to AprilTag detection pipeline
            self.limelight_instance.enable_websocket()
        else:
            print("No Limelights found!")

    def read_results(self):
        if self.limelight_instance:
            result = self.limelight_instance.get_latest_results()
            parsed_result = limelightresults.parse_results(result)

            if parsed_result is not None:
                for tag in parsed_result.fiducialResults:
                    print(f"AprilTag ID: {tag.fiducial_id}, Robot Pose: {tag.robot_pose_target_space}")

    def cleanup(self):
        if self.limelight_instance:
            self.limelight_instance.disable_websocket()
