@extends('layouts.app')

@section('content')
    <input type="hidden" id="id_ankete" value="{{$anketa->ID_ANKETE}}">
    <div class="container">
        <div class="row">
            <div class="col-md-8 col-md-offset-2">
                <h1 style="text-align: center">{{$anketa->IME}}</h1>
                <ul class="progress-indicator">
                    @foreach($casovi as $cas)
                        <li class="@if ($cas == $casovi[0])active @endif" id="ind_{{$cas->ID_CAS}}">
                            <span class="bubble"></span>
                            <i class="fa fa-check-circle"></i>
                            @foreach(preg_split("/[\s,_-]+/", $cas->predmet->IME) as $ch){{$ch[0]}}@endforeach
                            ({{$cas->TIP_CASA}})
                        </li>
                    @endforeach
                </ul>
                @foreach($casovi as $cas)
                    <div class="cas panel panel-default @if ($cas != $casovi[0]) hide @else visible @endif" id="cas_{{$cas->ID_CAS}}">
                        <input type="hidden" class="id_cas" value="{{$cas->ID_CAS}}">
                        <div class="panel-heading"><h3>{{$cas->predmet->IME}} ({{($cas->TIP_CASA == 'P') ? "Predavanje" : "Vežbe" }})</h3><h4>{{$cas->predavac->IME}} {{$cas->predavac->PREZIME}}</h4></div>

                        <ul class="list-group">
                            @foreach($pitanja as $pitanje)
                                <li class="list-group-item">

                                    <p>{{$pitanje->TEKST}} @if($pitanje->TIP_PITANJA == 'P')<i class="fa fa-asterisk text-danger" aria-hidden="true"></i>@endif</p>
                                    <form>
                                        <input type="hidden" class="id_pitanja" value="{{$pitanje->ID_PITANJA}}">
                                        @if($pitanje->TIP_PITANJA == 'P')
                                                <input type="hidden" name="qtype" value="P">
                                                @for($i = 0; $i < 5; $i++)
                                                    <label class="radio-inline">
                                                        <input type="radio" name="p{{$cas->ID_CAS}}_{{$pitanje->ID_PITANJA}}" value="{{$i+1}}">{{$i+1}}
                                                    </label>
                                                @endfor
                                        @else
                                            <input type="hidden" name="qtype" value="OP">
                                            <textarea style="width: 100%"></textarea>
                                        @endif
                                    </form>
                                </li>
                            @endforeach

                            <li class="list-group-item" style="min-height: 48px;">
                                @if ($cas != $casovi[0])<button class="prev-button">Prev</button>@endif
                                @if ($cas != $casovi[count($casovi)-1])<button class="next-button pull-right">Next</button> @else
                                        <button class="finish-button pull-right">Finish @endif</button>
                            </li>
                        </ul>
                    </div>
                @endforeach

               {{-- @foreach($opsta as $pitanje)
                    <li class="opste_pitanje">
                        {{$pitanje->TEKST}}
                        <textarea></textarea>
                    </li>
                @endforeach--}}
            </div>
        </div>
    </div>
@endsection

@section('js-src')
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
    <script src="{{ asset('js/anketa.js') }}"></script>
@endsection