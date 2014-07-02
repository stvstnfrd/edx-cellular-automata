import pkg_resources

from lms_mixin import LmsCompatibilityMixin
from xblock.core import XBlock
from xblock.fields import Scope, Boolean, Integer, List
from xblock.fragment import Fragment
from webob import Response
import json

class OLIAutomataXBlock(LmsCompatibilityMixin, XBlock):
    """
    XBlock wrapper for the Cellular Automata demo for OLI.
    """

    # Data Elements
    completed = Boolean(
        default=False,
        scope=Scope.user_state,
        help="Current problem state: have they clicked \"grade\" yet?"
    )
    errors = Integer(
        default=0,
        scope=Scope.user_state,
        help="Current problem state: if this has been graded, how many errors?"
    )
    genarray = List(
        default=[],
        scope=Scope.user_state,
        help="Current problem state: list of strings representing state of cells"
    )

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
        frag.initialize_js('OLIAutomataXBlock')
        return frag

    def studio_view(self, context=None):
        """
        How the instructor will change settings for this XBlock.
        """
        return Fragment("foo")


    # Data Accessors
    # Save, Load, and Grade endpoints that parallel how it's done in JSInput

    def unpack_datadict_save(self, data):
        if "completed" in data:
            self.completed = data['completed']
        if "errors" in data:
            self.errors = data['errors']
        if "genarray" in data:
            self.genarray = data['genarray']

    @XBlock.json_handler
    def save_state(self, data, suffix=''):
        """
        Data is a dict that the json_handler decoded for us already.  Just use the helper
        function to actually set the values, factored out so grade() can use it too.
        """
        self.unpack_datadict_save(data)

    @XBlock.handler
    def load_state(self, request, suffix=''):
        """
        Simple response with the current state for this xblock as string-encoded JSON.
        """
        response_data =  {
            "completed": self.completed,
            "errors": self.errors,
            "genarray": self.genarray,
        }
        return Response(json.dumps(response_data))

    @XBlock.json_handler
    def grade(self, data, suffix=''):
        """
        Save state, then update the "real" problem grade show it gets correctly added into the
        course grade

        TODO: currently you need to be perfect (zero errors) to get any credit, could make this
        partial.
        """
        self.unpack_datadict_save(data)
        if "errors" not in data:
            return
        if "completed" not in data:
            return
        grade = 0
        if data['completed'] == True and data['errors'] == 0:
            grade = 1
        self.runtime.publish(
            self,
            'grade',
            {
                'value': grade,
                'max_value': self.weight
            }
        )
        response_data =  {
            "completed": self.completed,
            "errors": self.errors,
            "genarray": self.genarray,
        }
        return response_data

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("OLI Automata",
             """<oli_automata/>"""),
            ]
