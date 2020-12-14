CREATE TABLE [gpuutilisation] (
  [host_name] varchar(255) NOT NULL,
  [subscription_id] varchar(255) NOT NULL,
  [resource_group_name] varchar(255) NOT NULL,
  [vm_id] varchar(255) NOT NULL,
  [vm_size] varchar(255) NOT NULL,
  [uuid] varchar(255) NOT NULL,
  [gpu_name] varchar(255),
  [gpu_utilisation] int NOT NULL,
  [power_drawn] int,
  [used_memory] int NOT NULL,
  [total_memory] int NOT NULL,
  [gpu_temperature] int,
  [processes] varchar(5000),
  [query_time] datetime DEFAULT (getdate()) NOT NULL
)
GO

