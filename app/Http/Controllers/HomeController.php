<?php

namespace App\Http\Controllers;

use App\Anketa;
use App\Odgovor;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class HomeController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $user = Auth::user();
        /*$aktivneAnkete = Anketa::where("OTVORENA_OD", "<=", Carbon::now())
            ->where("OTVORENA_DO", ">=", Carbon::now())
            ->whereDoesntHave('popunili', function ($q) use ($user){
                $q->where("POPUNIO_ANKETU.ID_STUDENT",$user->ID_STUDENT);
            }
        )->get();*/

        //ipak prikazi sve ankete
        //ako pokusa da udje u anketu reci da je vec popunjena
        $aktivneAnkete = Anketa::where("OTVORENA_OD", "<=", Carbon::now())
            ->where("OTVORENA_DO", ">=", Carbon::now())->get();

        $data = [
            'student' => $user,
            'aktivne_ankete' => $aktivneAnkete
        ];
        return view('home', $data);
    }

    public function anketa($id_ankete){
        $user = Auth::user();
        $anketa = Anketa::find($id_ankete);
        if ($anketa->OTVORENA_OD >= Carbon::now() || $anketa->OTVORENA_DO <= Carbon::now())
            return view('zatvorenaAnketa');
        $popunio = $anketa->popunili->contains($user->ID_STUDENT);
        if ($popunio)
            return view('popunjenaAnketa');
        $pitanja = $anketa->pitanja->whereIn('TIP_PITANJA',['P', 'PO']);
        $opstaPitanja = $anketa->pitanja->where('TIP_PITANJA','O');
        $casovi = $user->sviCasovi();
        return view('anketa', [
            'anketa' => $anketa,
            'pitanja' => $pitanja,
            'opsta' => $opstaPitanja,
            'casovi' => $casovi
        ]);
    }

    public function anketasubmit(Request $request, $id_anketa){
        $anketa = Anketa::find($id_anketa);
        $user = Auth::user();
        if ($anketa->OTVORENA_OD >= Carbon::now() || $anketa->OTVORENA_DO <= Carbon::now())
            return view('zatvorenaAnketa');
        $popunio = $anketa->popunili->contains($user->ID_STUDENT);
        if ($popunio)
            return view('popunjenaAnketa');

        $odgovori = [];
        $data = $request->all();
        foreach ($data as $cas => $casPitanja){
            foreach ($casPitanja as $pitanjeId => $odgovor_data){
                $odgovor = new Odgovor();
                $odgovor->ID_PITANJA = $pitanjeId;
                $odgovor->ID_CAS = $cas;
                $odgovor->ID_ANKETE = $id_anketa;
                if (is_numeric($odgovor_data))
                    $odgovor->OCENA = $odgovor_data;
                else
                    $odgovor->KOMENTAR = $odgovor_data;
                $odgovor->save();
                print_r($odgovor);
            }
        }
        $anketa->popunili()->attach($user->ID_STUDENT);
    }
}
