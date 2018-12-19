
CREATE TABLE sample_time (
	sample_number SERIAL PRIMARY KEY,
	sample_time   DATETIME);
	
CREATE TABLE actual_temperature (
	sample_number    BIGINT NOT NULL PRIMARY KEY,
	valid            BOOLEAN NOT NULL,
	temperature      DOUBLE,
	acquisition_time DATETIME,
	CONSTRAINT       `fk_actual_temperature_sample_time`
		FOREIGN KEY (sample_number) REFERENCES sample_time (sample_number)
		ON DELETE CASCADE
		ON UPDATE RESTRICT
);

CREATE TABLE target_temperature (
	sample_number    BIGINT NOT NULL PRIMARY KEY,
	valid            BOOLEAN NOT NULL,
	temperature      DOUBLE,
	acquisition_time DATETIME,
	CONSTRAINT       `fk_target_temperature_sample_time`
		FOREIGN KEY (sample_number) REFERENCES sample_time (sample_number)
		ON DELETE CASCADE
		ON UPDATE RESTRICT
);

CREATE TABLE outside_temperature (
	sample_number    BIGINT NOT NULL PRIMARY KEY,
	valid            BOOLEAN NOT NULL,
	temperature      DOUBLE,
	acquisition_time DATETIME,
	CONSTRAINT       `fk_outside_temperature_sample_time`
		FOREIGN KEY (sample_number) REFERENCES sample_time (sample_number)
		ON DELETE CASCADE
		ON UPDATE RESTRICT
);

CREATE TABLE battery_state (
	sample_number    BIGINT NOT NULL PRIMARY KEY,
	valid            BOOLEAN NOT NULL,
	state      		 VARCHAR(50),
	acquisition_time DATETIME,
	CONSTRAINT       `fk_battery_state_sample_time`
		FOREIGN KEY (sample_number) REFERENCES sample_time (sample_number)
		ON DELETE CASCADE
		ON UPDATE RESTRICT
);
