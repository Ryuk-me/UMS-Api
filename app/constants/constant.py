#########################################################
#                                                       #
#                       UMS URLS                        #
#                                                       #
#########################################################

# GET AND POST BOTH
UMS_LOGIN_URL = "https://ums.lpu.in/lpuums/"

# POST EMPTY BODY
UMS_AUTH_STATE_CHECK_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/Getquicklinks"
)
UMS_STUDENT_BASIC_INFO_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetStudentBasicInformation"
)
UMS_STUDENT_PHONE_NUMBER_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetStudentContactNo"
)
UMS_STUDENT_TIME_TABLE = "https://ums.lpu.in/LpuUms/Reports/frmStudentTimeTable.aspx"

UMS_MAKEUP_CLASSES_URL = "https://ums.lpu.in/lpuums/frmViewStudentMakeupAdjusment.aspx"

UMS_USER_MESSAGES = "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetStudentMessages"

UMS_USER_COURSE_SYLLABUS = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetStudentCourses"
)
UMS_ANNOUNCEMENT_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/AnnouncementDetails"
)
UMS_KNOW_YOUR_AUTHORITIES_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetHeads"
)
UMS_ATTENDANCE_SUMMARY_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/StudentAttendanceSummary"
)
UMS_ATTENDANCE_DETAILS_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/StudentAttendanceDetail"
)
UMS_ASSIGMENTS_MARKS_URL = "https://ums.lpu.in/lpuums/frmstudentdownloadassignment.aspx"

UMS_EXAM_SEATING_PLAN_URL = "https://ums.lpu.in/lpuums/frmSeatingPlan.aspx"

UMS_PENDING_ASSIGNMENTS_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetStudenPendingAssignments"
)
UMS_CGPA_TERM_WISE_URL = "https://ums.lpu.in/lpuums/StudentDashboard.aspx/TermWiseCGPA"

UMS_MARKS_TERM_WISE_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/TermWiseMarks"
)
UMS_HOME_PAGE_URL = "https://ums.lpu.in/LpuUms/default3.aspx"

UMS_PLACEMENT_DRIVES_URL = (
    "https://ums.lpu.in/lpuums/StudentDashboard.aspx/GetPlacementDrives"
)
UMS_HOSTELER_DETAILS_URL = (
    "https://ums.lpu.in/lpuums/Reports/frmStatementofAccounts.aspx"
)
UMS_ELECTRICITY_BILL_CHECK_URL = (
    "https://ums.lpu.in/lpuums/frmViewHostelElectricityUnitDetails.aspx"
)
UMS_HOSTEL_LEAVE_SLIP_URL = "https://ums.lpu.in/lpuums/frmHostelLeaveSlip.aspx"

UMS_INDIVIDUAL_ANNOUNCEMENT_URL = (
    "https://ums.lpu.in/mobile/frmDisplayAnnouncement.aspx?aid={}&tbl=StuGen"
)
UMS_ASSIGNMENT_UPLOADED_BY_TEACHER_URL = "http://assignments.lpu.in/Teacher/"

UMS_PLACEMENT_PORTAL_HOME_PAGE = (
    "https://ums.lpu.in/Placements/HomePlacementStudent.aspx"
)

UMS_PLACEMENT_PORTAL_DRIVE_REGISTRATION = (
    "https://ums.lpu.in/Placements/frmPlacementDriveRegistration.aspx"
)

UMS_PLACEMENT_LOGIN = "https://ums.lpu.in/Placements/"

#########################################################
#                                                       #
#                 REQUEST HEADERS AND STUFF             #
#                                                       #
#########################################################

USER_AGENT_ONLY = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}

USER_AGENT_FORM_URL_ENCODED = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Content-Type ": "application/x-www-form-urlencoded",
}

USER_AGENT_JSON = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Content-Type": "application/json",
}
