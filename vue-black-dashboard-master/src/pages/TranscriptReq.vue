<template>
  <div>
    <div>
      <h1>Transcript Request</h1>

      <h3>Course Catalog List</h3>
      <base-dropdown title-classes="btn btn-secondary" menu-classes="dropdown-black" title="Add a Course">
        <option
          v-for="course in courses"
          v-bind:key="course.id"
          class="dropdown-item"
          v-bind:value="course"
          @click="addCourse(course);"
          >{{ course.courseNum }}</option
        >
      </base-dropdown>
      <base-dropdown title-classes="btn btn-secondary" menu-classes="dropdown-black" title="Select Major">
        <option
          v-for="degree in degrees"
          v-bind:key="degree.major"
          class="dropdown-item"
          v-bind:value="degree"
          @click="selectDegree(degree);"
          >{{ degree.major }}</option
        >
      </base-dropdown>
      <br />
      <base-button type="default" @click="auditTranscript();"
        >Audit Transcript</base-button
      >
      <modal :show.sync="modals.auditModal" body-classes="p-0">
        <card
          type="secondary"
          header-classes="bg-white pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0"
        >
          <div class="text-muted text-center mb-3">
            <small>Transcript Audit Results</small>
          </div>
          <div v-if="this.reccommendations.length > 0">
            <h4>Reccommended Degrees Based on Your Progress: </h4>
          <ul > 
            <li v-for="reccommendation in reccommendations" v-bind:key="reccommendation.major">{{reccommendation.major}}</li>
            </ul>
          </div>
          <h4 v-if="this.selectedDegreeName !== ''">
            Major: {{ this.selectedDegreeName }}
          </h4>
          <h4 v-else>Major Not Selected</h4>
          <br /><br />
          <base-table :data="auditedTranscript">
            <template slot="columns">
              <th>Requirements</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.name }}</td>
              <td>
                <base-table :data="row.complete">
                  <template slot="columns">
                    <th>Completed Courses</th>
                  </template>
                  <template slot-scope="{ row }">
                    <td>{{ row }}</td>
                  </template>
                </base-table>
              </td>
              <td v-if="!row.requirement_met">
                <base-table :data="row.incomplete">
                  <template slot="columns">
                    <th>Incomplete Courses</th>
                  </template>
                  <template slot-scope="{ row }">
                    <td>{{ row }}</td>
                  </template>
                </base-table>
              </td>
              <td v-if="!row.requirement_met">{{ row.remaining }} Remaining</td>
              <td v-else>Requirement Satisified</td>
            </template>
          </base-table>
        </card>
      </modal>
      <div>
        <h3>Selected Degree:  
        <span v-if="this.selectedDegreeName !== ''">{{
          this.selectedDegreeName
        }}</span>
        <span v-else>None</span></h3>

      </div>
      <div>
        <br />
        <h3>Selected Courses</h3>

        <base-table :data="displayedCourses">
          <template slot="columns">
            <th class="text-center">#</th>
            <th>Name</th>
            <th>Credits</th>
            <th>Prerequisites</th>
            <th>Course Number</th>
            <th>Offered In</th>
            <th>Department</th>
            <th>Description</th>
            <th></th>
          </template>
          <template slot-scope="{ row }">
            <td>{{ row.id }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.credit }}</td>
            <td>{{ row.prereqs }}</td>
            <td>{{ row.courseNum }}</td>
            <td>{{ row.offeredIn }}</td>
            <td>{{ row.department }}</td>
            <td>{{ row.description }}</td>
            <td class="td-actions text-right">
              <base-button
                type="danger"
                size="sm"
                icon
                @click="removeCourse(row.id);"
              >
                <i class="tim-icons icon-simple-remove"></i>
              </base-button>
            </td>
          </template>
        </base-table>
      </div>
      <br />
      <a id="dummy"></a>
      <button id="dwn" v-on:click="downloadCSV();">Download as CSV</button>
      <button id="dwn" v-on:click="downloadJSON();">Download as JSON</button>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Modal from "@/components/Modal";
import _ from "lodash";
import { BaseTable } from "@/components";

const BASE_URL = "http://localhost:5000";

export default {
  components: {
    BaseTable,
    Modal
  },

  data() {
    return {
      user: {
        major: "",
        courses: []
      },
      displayedCourses: [],
      courses: [],
      degrees: [],
      modals: {
        auditModal: false
      },
      auditedTranscript: [],
      reccommendations: [],
      columns: [
        "id",
        "name",
        "credits",
        "offeredIn",
        "description",
        "department"
      ],
      selectedDegree: {},
      selectedDegreeName: ""
    };
  },

  methods: {
    /**
     * The method takes in a course object, and adds it to the user state array
     */
    addCourse(course) {
      // checking if the object already exists in the array
      if (this.displayedCourses.indexOf(course) === -1) {
        this.displayedCourses.push(course);
        this.user.courses.push(course.courseNum);
      }
    },

    /**
     * This method allows a user to remove a course based on the course ID number
     */
    removeCourse(id) {
      for (let i = 0; i < this.user.courses.length; i++) {
        if (this.displayedCourses[i].id === id) {
          // this removes a course by a given index
          this.user.courses.splice(i, 1);
          this.displayedCourses.splice(i, 1);
        }
      }
    },

    /**
     * This course selects a degree that a user chooses
     */
    selectDegree(degree) {
      this.selectedDegree = degree;
      this.selectedDegreeName = degree.major;
    },

    /**
     * This method is called when a user audits a transcript.
     * It displays a modal that shows the audited transcript response.  It displays what
     * the user has completed and still needs to complete
     */
    auditTranscript() {
      this.modals.auditModal = true;

      // we only want to call the
      if (this.selectedDegree !== undefined) {
        let request = {};
        request["transcript"] = {};
        this.user.major = this.selectedDegreeName;
        request.transcript["major"] = this.selectedDegreeName;
        request.transcript["courses"] = this.user.courses;
        this.upload(request);
      }
    },

    /**
     * This function handles the uploading of form data to the backend
     */
    upload(formData) {
      console.log(formData);
      const url = `${BASE_URL}/transcript`;
      return (
        axios
          .post(url, formData)
          // retrieve data
          .then(res => {
            return res.data;
          })
          .then(res => {
            this.auditedTranscript = res.audit;
            this.reccommendations = [];
           /**
             * Converting each JSON string representation of a degree into a degree object
             */            
            for (let i = 0; i < res.reccommendations.length; i++) {
                this.reccommendations.push(JSON.parse(res.reccommendations[i]));
            }
            console.log(res)
            console.log(this.auditedTranscript);
          })
      );
    },
    downloadCSV() {
      var csv =
        "ID,name,credits,prereqs,courseNum,offeredIn,description,department\r\n";
      this.displayedCourses.forEach(function(row) {
        csv +=
          row.id +
          ',"' +
          row.name +
          '",' +
          row.credits +
          ',"' +
          row.prereqs +
          '",' +
          row.courseNum +
          "," +
          row.offeredIn +
          ',"' +
          row.description +
          '",' +
          row.department;
        csv += "\r\n";
      });

      var hiddenElement = document.getElementById("dummy");
      hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(csv);
      hiddenElement.target = "_blank";
      hiddenElement.download = "courses.csv";
      hiddenElement.click();
    },
    downloadJSON() {
      var major = this.selectedDegreeName;
      var json =
        ' {\r\n\t"transcript": {\r\n\t\t"major": "' +
        major +
        '",\r\n\t\t"courses": [';

      this.displayedCourses.forEach(function(row) {
        json += '\r\n\t\t"' + row.courseNum + '",';
      });
      json = json.substring(0, json.length - 1);
      json += "\r\n\t\t]\r\n\t}\r\n}";

      var hiddenElement = document.getElementById("dummy");
      hiddenElement.href = "data:text/json;charset=utf-8," + encodeURI(json);
      hiddenElement.target = "_blank";
      hiddenElement.download = "courses.json";
      hiddenElement.click();
    }
  },

  mounted() {
    axios
      .get("http://127.0.0.1:5000/coursecatalog")
      .then(res => {
        return JSON.parse(res.data);
      })
      .then(res => {
        this.courses = res.courses;

        this.courses.sort( (a,b) => {
          let comparison = 0;

          if (a.courseNum > b.courseNum) {
            comparison = 1;
          } else if (a.courseNum < b.courseNum){
            comparison = -1;
          }

          return comparison;
        })
      });

    axios
      .get("http://127.0.0.1:5000/degreecatalog")
      .then(res => JSON.parse(res.data))
      .then(res => {
        this.degrees = res.degrees;

      });
  }
};
</script>
<style lang="scss">
button {
  background-color: rgb(56, 239, 125);
  border: none;
  color: black;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

#dwn {
  padding: 2em;
  margin-right: 1em;
  margin-top: 1em;
  border-radius: 8px;
}
</style>
