package org.example.web1.idmPojo;

import java.util.LinkedHashMap;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import org.example.web1.model.Employee;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "employee_age",
        "employee_name",
        "employee_salary",
        "id",
        "profile_image"
})
public class IdmEmployeePojo {

    @JsonProperty("employee_age")
    private Integer employeeAge;
    @JsonProperty("employee_name")
    private String employeeName;
    @JsonProperty("employee_salary")
    private Integer employeeSalary;
    @JsonProperty("id")
    private Integer id;
    @JsonProperty("profile_image")
    private String profileImage;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new LinkedHashMap<String, Object>();

    @JsonProperty("employee_age")
    public Integer getEmployeeAge() {
        return employeeAge;
    }

    @JsonProperty("employee_age")
    public void setEmployeeAge(Integer employeeAge) {
        this.employeeAge = employeeAge;
    }

    @JsonProperty("employee_name")
    public String getEmployeeName() {
        return employeeName;
    }

    @JsonProperty("employee_name")
    public void setEmployeeName(String employeeName) {
        this.employeeName = employeeName;
    }

    @JsonProperty("employee_salary")
    public Integer getEmployeeSalary() {
        return employeeSalary;
    }

    @JsonProperty("employee_salary")
    public void setEmployeeSalary(Integer employeeSalary) {
        this.employeeSalary = employeeSalary;
    }

    @JsonProperty("id")
    public Integer getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(Integer id) {
        this.id = id;
    }

    @JsonProperty("profile_image")
    public String getProfileImage() {
        return profileImage;
    }

    @JsonProperty("profile_image")
    public void setProfileImage(String profileImage) {
        this.profileImage = profileImage;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString(){
        return String.format("Employee: Id=%d, Name=%s, Age=%d",
                this.id, this.employeeName, this.employeeAge);
    }

    public Employee toEmployee() {
        return new Employee(this.id.toString(), this.employeeName);
    }

}