# Backend tips

## Alembic guide

After creating the migration please do:

1. Reorder columns
2. Remove autogenerated foreign keys constraints if composite ones were created explicitly 
with __table_args__ like here
    ```python
    # sa.ForeignKeyConstraint(['frame_time_point'], ['frames.time_point'], ),
    sa.ForeignKeyConstraint(['frame_video_id', 'frame_time_point'], ['frames.video_id', 'frames.time_point'], ),
    # sa.ForeignKeyConstraint(['frame_video_id'], ['frames.video_id'], ),
   ```
3. Add enum drop to the downgrade section if a new enum data type will be created after the migration
    ```python
       def downgrade():
         op.execute("""DROP TYPE name_of_enum""")
    ```
   
## Useful links
### Auth implementation
https://testdriven.io/blog/fastapi-jwt-auth/
