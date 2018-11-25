namespace py kv

service KVService
{
    string create(1:string value),
    string read(1:string obj_id),
    string update(1:string obj_id, 2:string value),
    void delete_doc(1:string obj_id),
}
