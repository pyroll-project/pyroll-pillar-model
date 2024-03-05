from pyroll.core import RollPass


@RollPass.OutProfile.cross_section
def rp_out_cross_section(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.cross_section


@RollPass.OutProfile.width
def rp_out_width(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.cross_section.width
