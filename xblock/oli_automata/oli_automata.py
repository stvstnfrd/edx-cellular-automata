import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Dict
from xblock.fragment import Fragment

class OLIAutomataXBlock(XBlock):
    """
    XBlock wrapper for the Cellular Automata demo for OLI.
    """

    # Data Elements

    exercise_state = Dict(default={}, scope=Scope.user_state, help="State of exercise")
    grade = Integer(default=0, scope=Scope.user_state, help="Grade")


    # Helper Functions

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    # Views -- Student (rendering) and Studio (configuring)

    def student_view(self, context=None):
        """
        How the student will see this XBlock, usually in the LMS.
        """
        html = self.resource_string("static/html/oli_automata.html")
        frag = Fragment(html.format(self=self))
        frag.add_content(self.resource_string("static/html/oli_buttons.html"))
        frag.add_css(self.resource_string("static/css/oli_automata.css"))
        frag.add_javascript(self.resource_string("static/js/src/oli_automata.js"))
        frag.add_javascript(self.resource_string("static/js/src/oli_buttons.js"))
        return frag

    def studio_view(self, context=None):
        """
        How the instructtor will change settings for this XBlock.
        """
        return Fragment("foo")


    # Data Accessors
    # Save, Load, and Grade endpoints that parallel how it's done in JSInput

    @XBlock.json_handler
    def save_state(self, new_state):
        self.exercise_state = new_state
        return new_state

    @XBlock.json_handler
    def load_state(self):
        return self.exercise_state

    @XBlock.json_handler
    def grade(self, grade_state):
        if error in grade_state:
            self.grade = (grade_state["error"] == 0)

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("OLI Automata",
             """<vertical_demo>
    <oli_automata/>
</vertical_demo>"""),
            ]
