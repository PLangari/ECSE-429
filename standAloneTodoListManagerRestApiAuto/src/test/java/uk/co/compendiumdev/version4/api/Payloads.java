package uk.co.compendiumdev.version4.api;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class Payloads {

    public static class ProjectPayload{
        public String id;
        public String title;
        public Boolean completed;
        public Boolean active;
        public String description;
        public List<IdValues> tasks;
    }

    public static class IdValues {
        public String id;
    }

    public static class ProjectsPayload{
        public List<ProjectPayload> projects;
    }

    public static class TodoPayload{
        public String id;
        public String title;
        public Boolean doneStatus;
        public String description;
        public List<IdValues>tasksof;
    }

    public static class TodosPayload{
        public List<TodoPayload> todos;
    }

    public static class ErrorMessageResponse {
        public List<String> errorMessages;
    }
}

