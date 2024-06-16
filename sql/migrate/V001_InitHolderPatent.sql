-- Create HOLDER_ENTITY table
CREATE TABLE HOLDER_ENTITY (
    company_id BIGSERIAL PRIMARY KEY,
    full_name TEXT,
    shorten_name TEXT,
    okved TEXT,
    classification VARCHAR(255),
    tin BIGSERIAL,
    psrn BIGSERIAL,
    is_active_company BOOLEAN NOT NULL
--     id_of_heir BIGSERIAL,
--     CONSTRAINT fk_heir FOREIGN KEY (id_of_heir) REFERENCES HOLDER_ENTITY (company_id)
);

-- Create PATENT table
CREATE TABLE PATENT_MODEL (
    registration_number BIGSERIAL PRIMARY KEY,
    publish_date DATE NOT NULL,
    description TEXT,
    authors TEXT,
    patent_holders TEXT,
    is_active BOOLEAN NOT NULL
);

-- Create PATENT table
CREATE TABLE PATENT_INVENTION (
    registration_number BIGSERIAL PRIMARY KEY,
    publish_date DATE NOT NULL,
    description TEXT,
    authors TEXT,
    patent_holders TEXT,
    is_active BOOLEAN NOT NULL
);

-- Create PATENT table
CREATE TABLE PATENT_DESIGN (
    registration_number BIGSERIAL PRIMARY KEY,
    publish_date DATE NOT NULL,
    description TEXT,
    authors TEXT,
    patent_holders TEXT,
    is_active BOOLEAN NOT NULL
);

-- Create a junction table to handle the many-to-many relationship
CREATE TABLE PATENT_MODEL_HOLDER (
    patent_id BIGSERIAL NOT NULL,
    company_id BIGSERIAL NOT NULL,
    PRIMARY KEY (patent_id, company_id),
    CONSTRAINT fk_patent FOREIGN KEY (patent_id) REFERENCES PATENT_MODEL (registration_number),
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES HOLDER_ENTITY (company_id)
);

-- Create a junction table to handle the many-to-many relationship
CREATE TABLE PATENT_INVENTION_HOLDER (
    patent_id BIGSERIAL NOT NULL,
    company_id BIGSERIAL NOT NULL,
    PRIMARY KEY (patent_id, company_id),
    CONSTRAINT fk_patent FOREIGN KEY (patent_id) REFERENCES PATENT_INVENTION (registration_number),
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES HOLDER_ENTITY (company_id)
);

-- Create a junction table to handle the many-to-many relationship
CREATE TABLE PATENT_DESIGN_HOLDER (
    patent_id BIGSERIAL NOT NULL,
    company_id BIGSERIAL NOT NULL,
    PRIMARY KEY (patent_id, company_id),
    CONSTRAINT fk_patent FOREIGN KEY (patent_id) REFERENCES PATENT_DESIGN (registration_number),
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES HOLDER_ENTITY (company_id)
);