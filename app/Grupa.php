<?php
/**
 * User: Nikol
 * Date: 16.7.2017.
 * Time: 16.29
 */

namespace App;


use Illuminate\Database\Eloquent\Model;

class Grupa extends Model
{
    protected $table = "GRUPA";
    protected $primaryKey = "ID_GRUPA";
    public $timestamps = false;

    public function casovi(){
        return $this->belongsToMany(Cas::class, "GRUPE_NA_CASU", "ID_GRUPA", "ID_CAS");
    }
}