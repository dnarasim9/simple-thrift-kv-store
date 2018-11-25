namespace py kv

service KVService
{
    string create(1:string value),
    string read(1:string obj_id),
}
