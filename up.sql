
--A syntactically valid PDDL domain. 
CREATE TABLE Domains (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    loop_number INTEGER NOT NULL,
    label TEXT NOT NULL,
    raw_pddl TEXT NOT NULL
);

-- A description of a domain, predicate, action, etc, along with an associated class.
CREATE TABLE Descriptions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nl TEXT NOT NULL,
    nl_class TEXT NOT NULL
);

CREATE TABLE DomainDescriptionOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL REFERENCES Domains(id),
    description_id INTEGER NOT NULL REFERENCES Descriptions(id)
);

-- CREATE TABLE Types (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     label TEXT NOT NULL,
-- );

-- CREATE TABLE SuperTypes (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     sub_type_id INTEGER NOT NULL REFERENCES Types(id),
--     domain_id INTEGER NOT NULL REFERENCES Domains(id)
-- );

-- CREATE TABLE TypeOwners (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     type_id INTEGER NOT NULL REFERENCES Types(id),
--     domain_id INTEGER NOT NULL REFERENCES Domains(id)
-- )

CREATE TABLE Predicates (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL
);

CREATE TABLE PredicateOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL REFERENCES Domains(id),
    predicate_id INTEGER NOT NULL REFERENCES Predicates(id)
);

CREATE TABLE PredicateDescriptionOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    predicate_id INTEGER NOT NULL REFERENCES Predicates(id),
    predicate_description_id INTEGER NOT NULL REFERENCES Descriptions(id)
);

-- CREATE TABLE PredicateArgs (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     label TEXT NOT NULL,
--     pos INTEGER NOT NULL,
--     predicate_id INTEGER NOT NULL REFERENCES Predicates(id),
--     type_id INTEGER NOT NULL REFERENCES Types(id)
-- );

CREATE TABLE Actions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL
);

CREATE TABLE ActionOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL REFERENCES Domains(id),
    action_id INTEGER NOT NULL REFERENCES Actions(id)
);

CREATE TABLE ActionDescriptionOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    action_id INTEGER NOT NULL REFERENCES Actions(id),
    action_description_id INTEGER NOT NULL REFERENCES Descriptions(id)
);

-- CREATE TABLE ActionArgs (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     label TEXT NOT NULL,
--     pos INTEGER NOT NULL,
--     action_id INTEGER NOT NULL REFERENCES Actions(id),
--     type_id INTEGER NOT NULL REFERENCES Types(id)
-- );

-- CREATE TABLE ActionPreds (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     precondition BOOLEAN NOT NULL,
--     negated BOOLEAN NOT NULL,
--     action_id INTEGER NOT NULL REFERENCES Actions(id),
--     predicate_id INTEGER NOT NULL REFERENCES Predicates(id)
-- );

-- CREATE TABLE ActionPredArgs (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     pos INTEGER NOT NULL,
--     action_predicate_id INTEGER NOT NULL REFERENCES ActionPreds(id),
--     predicate_arg_id INTEGER NOT NULL REFERENCES ActionArgs(id)
-- );

CREATE TABLE DomainTemplates (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    raw_text TEXT NOT NULL
);

CREATE TABLE DomainTemplateOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL REFERENCES Domains(id),
    template_id INTEGER NOT NULL REFERENCES DomainTemplates(id)
);

CREATE TABLE Problems (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    raw_pddl TEXT NOT NULL
);

CREATE TABLE ProblemOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL REFERENCES Domains(id),
    problem_id INTEGER NOT NULL REFERENCES Problems(id)
);

CREATE TABLE Plans (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    raw_text TEXT NOT NULL
);

CREATE TABLE PlanOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL REFERENCES Problems(id),
    plan_id INTEGER NOT NULL REFERENCES Plans(id)
);

CREATE TABLE Prompts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    model_style TEXT NOT NULL, --Either chat completion or text completion
    raw_prompt TEXT NOT NULL,
    loop_id INTEGER NOT NULL
);

-- A model request is a request that is actually sent to the LLM,
-- It associates a prompt with a specific model and parameters to that model.
CREATE TABLE ModelRequests (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    loop_id INTEGER NOT NULL, --The id of the loop that this request is part of
    model_name TEXT NOT NULL, --HF like model: provider/model 
    api_provider TEXT NOT NULL, --Identifies the API endpoint to use
    raw_json TEXT NOT NULL --api-provider specific prompt 
);

CREATE TABLE ModelRequestOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL REFERENCES Prompts(id),
    model_request_id INTEGER NOT NULL REFERENCES ModelRequests(id)
);

CREATE TABLE ModelResponses (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    raw_response TEXT NOT NULL
);

CREATE TABLE ModelResponseOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    model_request_id INTEGER NOT NULL REFERENCES ModelRequests(id),
    model_response_id INTEGER NOT NULL REFERENCES ModelResponses(id)
);

-- Each result corresponds to exactly one model response
CREATE TABLE Results (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL REFERENCES ModelResponses(id),
    class TEXT NOT NULL,
    subclass INTEGER NOT NULL,
    msg TEXT NOT NULL
);

CREATE TABLE ResultOwners (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    model_response_id INTEGER NOT NULL REFERENCES ModelResponses(id),
    result_id INTEGER NOT NULL REFERENCES Results(id)
);