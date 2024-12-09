from peewee import *
import os

# Database setup - using SQLite to store machine logs
db = SqliteDatabase('machine_logs.db')

# Base model for all database tables
class BaseModel(Model):
    class Meta:
        database = db  

# Table to store machine status
class MachineStatus(BaseModel):
    machine_id = CharField() 
    name = CharField()       
    status = CharField()     
    last_updated = DateTimeField() 

# Table to store log entries for machines
class Log(BaseModel):
    machine_id = CharField()  
    log_level = CharField()   
    message = TextField()     
    created_at = DateTimeField()  

# Initialize the database connection
db.connect()

# Create the tables if they do not already exist
db.create_tables([MachineStatus, Log])
