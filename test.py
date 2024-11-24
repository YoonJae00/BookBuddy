import requests

url = "http://localhost:8000/api/v1/novels/"

# 소설 내용을 직접 문자열로 작성
novel_content = """=======================================
템빨 1권
=======================================
프롤로그


“5분 남았습니다!”

코크로 섬 던전 4층.

통합 랭킹 16위 극검을 필두로 한 상위 랭커 8명이 한자리에 모였다. 그들의 뒤로는 은기사 길드의 정예 200명이 도열해 있었다.

작은 요새를 점령할 수도 있을 전력이 한데 모였으니 실로 장관이다.

하지만 그들로서도 부족하다는 듯이, 모두의 얼굴에는 긴장감과 불안감만이 가득했다.

“4분 남았습니다!”

점차 시간이 다가올수록 길드원들의 초조함이 극에 달했다. 안절부절못하며 다리를 떨거나 손톱을 물어뜯는 이도 있었다.

그들을 둘러본 극검은 말없이 시선을 내렸다. 검을 쥐고 있는 손에 식은땀이 흥건했다.

‘도무지 진정이 안 되는군.’

코크로 섬 던전은 은기사 길드가 완벽하게 통제하고 있었다. 2주에 단 한 번 4층에 출현하는 보스 몬스터, 헬가오를 독식하기 위함이었다.

하지만 헬가오가 예상보다 강력하고 패턴이 다양한 탓에, 여태까지 5번의 원정 중 단 한 차례도 공략에 성공하지 못한 실정이었다.

극검과 은기사의 정예들은 다음번엔 기필코 성공하겠다는 일념으로 지난 한 달간 현금으로 아이템을 강화하고 시간을 쥐어짜 레벨을 올려 왔다.

투자한 만큼 확실하게 강해진 전력이건만, 헬가오의 막강함을 절실히 알고 있는 그들은 섣부른 자신감을 가질 수가 없었다.

“3분 남았습니다!”

앞으로 3분 후면 헬가오가 등장하면서 이곳이 온통 불바다로 변하리라. 이 중 몇은 그 불길조차 감당하지 못하고 죽게 되리라.

“2분 남았습니다!”

뜨거운 열기가 서서히 피어오르며 공간을 지배하기 시작했다.

‘제기랄.’

모두에게 용기를 북돋아 줘야 할 위치인 극검이 오히려 두려움에 휩싸였다.

묵색 불꽃을 전신에 두르고, 열풍을 일으키는 지팡이를 휘둘러 대는 헬가오의 압도적인 모습이 명확하게 상기된 탓이었다.

‘놈을 해치우기엔 아직도 우리의 전력이 부족하지 않을까?’

10위권 최상위 랭커의 힘이 보태진다면 혹 모를까, 자신들만의 힘으로는 이번 원정 역시 실패하리라는 생각을 지울 수가 없었다.

하지만 길드 내 최고의 랭커인 자신이 나약한 모습을 보일 수도 없었기에 극검은 이를 악물고 공포를 견뎌 냈다.

‘해내자. 해낼 수 있다. 우리는 강하다!’

마음을 다잡은 극검이 각종 버프 물약을 복용하기 시작하자 다른 이들도 그를 따랐다.

바로 그때였다.

“1분 남았… 엇? 침입자! 침입자랍니다!!”

“뭐라고?”

길드원 전원의 시선이 입구로 향했다.

한 청년이 혈혈단신으로 입장하고 있었다.

무기도, 갑옷도 무장하지 않고 망토 하나 휘두른 모습이 이색적이었다.

‘저 꼴로 아래층의 수비 병력을 단신으로 돌파했단 말인가?’

고도로 단련된 어쌔신일까? 

아니다. 어쌔신이 저렇게 모습을 드러내 놓고 다닐 리 없다. 

극검은 청년의 머리 위에 떠 있는 이름을 몇 번이나 곱씹어 보았다. 하지만 기억의 편린을 아무리 뒤져 봐도 낯설기만 했다.

‘랭커도 아닌데?’

극검이 다른 동료들에게 저치를 아느냐고 눈짓했지만 다들 하나같이 고개를 저을 뿐이었다.

‘별것도 아닌 녀석을 여기까지 들이다니, 경계병들이 농땡이를 피우고 있었나 보군. 한심한.’

그렇게 결론짓고 얼굴을 찌푸린 극검이 청년에게 경고했다.

“여기는 우리 은기사 길드가 통제하고 있는 구역이다. 어찌 예까지 오를 수 있었는지는 모르겠다만, 죽고 싶지 않다면 썩 돌아가라.”

“은신이 갑자기 왜 풀렸나 했더니 헬가오에게 감지당한 탓이었나?”

극검의 경고를 가볍게 무시한 청년이 혼잣말을 하면서 망토를 벗어던졌다.

“오오!”

곳곳에서 감탄사가 터져 나왔다.

빠른 속도로 청년의 전신에 장착되기 시작하는 갑옷의 외관이 상당히 멋졌기 때문이다.

금속 재질임에도 불구하고 맞춤 정장인 양 착용자의 핏을 완벽하게 살려 주었고, 매끄러운 표면은 어찌나 반들거리는지 거울로도 활용할 수 있을 듯했다. 

적색과 흑색, 그리고 금색이 격조 있는 조화를 이루어 품격을 표출했다.

특히 개성적인 점은 꼬리뼈 부근에 뻗어 나온 1미터 길이의 꼬리였다. 칼날처럼 날카로운 그것은 놀랍게도 스스로 움직이고 있었다.

“뭐, 뭐야, 저 갑옷?”

“겁나 멋있네……. 유니크인가?”

생전 처음 보는 형식의 갑옷을 목격하고 놀란 길드원들이 흥미를 억제하지 못하고 수군거렸다. 

그에 발끈한 극검이 언성을 높였다.

“지금 그딴 게 중요하냐! 당장 저놈을 쫓아내지 않고 뭐 하는 거냐!”

잠시 후면 헬가오가 등장한다. 그리고 던전에서 탈출할 수 없게 된다. 그 전에 거슬리는 외부인을 처리해야만 했다.

갑옷에 대한 관심을 일단 접어 둔 길드원들이 극검의 명령을 받들어 실행에 옮기려는 순간이었다.

쿠오오오오오!!!



[지옥불의 주인 헬가오가 출현합니다.]

[헬가오의 포효로 인해 공포, 혼란, 쇠약 효과가 적용됩니다.]

[헬가오의 열기로 인해 화염 저항력이 50퍼센트 하락합니다.]

[솟아오른 불기둥이 당신을 덮칩니다.]



“크악!!”

“히이익!”

전신을 휘감고 있는 묵색 불길 탓에 형체조차 알아볼 수 없는 괴수가 등장하자 길드원들 중 절반이 빈사 상태에 빠지거나 불타 죽어 버렸다. 

간신히 버티고 선 절반의 인원 중에서도 멀쩡한 이가 드물었다.

극검은 떠오른 알림창을 보고 경악했다.

‘화염 저항력을 86프로까지 올렸는데도 이 정도 피해라니……!’

이번에도 실패다.

그것을 직감한 극검이 절망하던 중, 문득 자신의 두 눈을 의심했다.

정체 모를 청년.

다른 이들은 모두 화염에 휩싸여 어찌할 바 모르고 있는 와중에, 그는 홀로 멀쩡히 앞으로 나아가고 있었다. 걸음걸이에서 여유가 느껴질 정도로 그는 태연했다.

“어, 어떻게… 헉?”

이어진 광경을 목격한 극검은 어처구니가 없어서 말문을 닫아 버렸다.

헬가오가 날뛰며 다른 이들을 무참하게 살육하고 있는 이때 청년은 곡괭이를 쥐어 들었다. 그리고 한쪽 벽에 다가가서는 곡괭이질을 시작하는 게 아닌가?

까앙! 까앙!

매우 능숙한 폼으로 곡괭이질을 하던 청년이, 턱 선을 타고 흘러내린 땀방울을 닦아 내면서 투덜거렸다.

“어휴, 더워! 우라질, 노가다가 점점 더 빡세지잖아? 어떻게 생겨 먹은 광물이 보스 몹 뜰 때만 나타난다는 거야? 이러다간 곡괭이 들고 드래곤 레어에 찾아가야 하는 날도 오겠네!”

때마침 헬가오가 휘두른 지팡이의 열풍이 청년의 뒤를 덮쳤다.

극검은 빈틈이 완벽하게 노려진 청년이 당연히 커다란 피해를 입고 쓰러질 줄로만 알았다. 

하지만 믿겨지지 않게도 청년은 아주 경미한 상처만 입었을 뿐이었다. 

“저기요, 아저씨.”

곡괭이질을 멈춘 청년이 처음으로 극검에게 시선을 돌렸다. 그리고 짜증스러운 표정을 짓고 말했다.

“저 자식 좀 어서 어떻게 해 봐요. 안 그래도 더워 죽겠는데 더 더워지잖아요.”

지금 자신이 헛것을 보고 있는 것인가?

멍하니 있던 극검이 뒤늦게 정신을 차리고 물었다.

“너는 어떻게 멀쩡할 수 있는 거지?”

청년은 뭐 그런 당연한 걸 묻느냐는 듯이 대수롭지 않게 대꾸했다. 

“템빨요.”

채챙! 챙!

청년의 갑옷에 달린 꼬리가 스스로 움직이며 헬가오의 지팡이에 맞서 싸우고 있었다.

그 모습에 극검은 벌어진 입을 다물지 못했다.


=======================================
제1장

원치 않았던 전직


자그마치 세 달간의 여정 끝에 발견한 ‘북쪽 끝의 동굴’에 입장한 나는 온갖 무구가 산처럼 쌓여 있는 압도적인 광경을 목격할 수 있었다.

“우와, 쩌네!”

찬란한 무구들의 이름은 기본이 녹색부터였다. 노란색과 보라색 이름도 심심찮게 보였다. 이 중 몇 가지만 챙겨 가도 갑부가 될 수 있을 터!

득달같이 달려든 나는 무구들을 닥치는 대로 쓸어 담으려 했지만 불가능했다.

[가질 수 없는 물품입니다.]

“하여튼 더럽게 쪼잔해요.”

눈앞에 분명 존재함에도 불구하고 획득할 수 없는 아이템들! 

가방에 집어넣고, 넣고, 다시 또 넣어 봐도 제자리로 돌아가 버리는 것이 마치 신기루 같다.

이런 상황을 두고 그림의 떡, 혹은 남의 마누라라고 하는 거구나. 

아니, 남의 마누라는 그림의 떡과 개념이 다르지.

결국 손가락만 빨면서 바라보고 있자니 강한 미련이 남았다. 

‘하긴… 이것들을 유저가 챙길 수 있다면 Satisfy의 경제 밸런스가 무너질 수도 있겠지. 아쉽지만 납득해 주마.’

애초에 내가 이곳까지 찾아온 이유는 이 무구들 때문이 아니었다. 

어차피 얻을 수 없는바, 마음을 달래고 관심을 돌린 나는 무구의 산을 기어올랐다. 그리고 번쩍이는 황금 탁자 위에 고고히 놓여 있는 한 권의 낡은 책과 대면했다.

“드디어…….”

여기까지 오면서 겪었던 온갖 고초가 주마등처럼 스쳐 지나갔다. 웃음이 나오는 것은 기본이요, 코끝이 찡해지면서 눈물까지 핑 돌았다. 

내가 끈기 하난 끝내줘서 망정이지, 보통 사람 같았으면 더럽다고 게임을 접어 버렸을 만큼 극악의 난이도를 자랑했던 퀘스트다. 그만한 퀘스트의 클리어를 목전에 둔 내가 스스로 대견하게 느껴졌다. 

“큭큭… 푸하하하핫!! 드디어 찾았다아아아!! 오우예에에엣!!”

중도 포기조차 불가능한 빌어먹을 S급 퀘스트! 

우연히, 그것도 강제적으로 떠안게 된 이 엿 같은 솔로 퀘스트 탓에 벌써 몇 번의 렙따를 경험했던가? 몇 개의 아이템이 내구력 손상으로 파괴되었던가!

인간이면서 드워프의 기술을 초월한 대장장이, 파그마의 신기(神技)가 집대성되어 있다는 비서!

이거 찾아오라고 에트날 왕국의 5대 금역을 누비게 만든 썩을 아슈르 백작 놈의 능글능글한 면상이 떠올랐다.

“고 쉐끼, 이것만 가져다주면 태양의 검을 준다고 했겠다? 그것만 받으면 너 따위 놈 평생 상종도 안 할 거다, 개자식! 나를 이렇게 뺑이 치게 만들다니!”

밀물처럼 밀려오는 쾌감을 느끼면서 다짐한 나는 책을 집어 들었다.



[전설적 장인의 기서 획득!]

[미감정 상태입니다. 플라리안의 눈을 사용하여 감정하면 상세 정보를 확인할 수 있습니다.] 

[플라리안의 눈을 사용하시겠습니까?]



“플라리안의 눈? 고작 퀘템 확인하는 데 최고급 감정 아이템이 필요하다고?”

플라리안의 눈은 현존하는 감정 아이템 중에서 가장 고가의 아이템이었다. 

반년 전에 혹시나 득템할 때를 대비해서 딱 하나 미리 구입해 놨으나, 슬프게도 득템을 못한 탓에 쓸 일이 없어서 여태껏 인벤토리 한편에 고이 모셔 두고 있었다.

“고작 퀘템 감정하는 일에 쓰긴 아까운데…….”

감정을 보류한 나는 황금 탁자를 살펴보았다. 

이 황금 덩어리를 어떻게든 챙겨 갈 방법이 없을까 강구했지만 꿈쩍도 않는다. 발로 차고, 두 손으로 힘껏 잡아당겨 보기도 하고, 이로 물어뜯어 보아도 부질없었다. 

다른 무구들과 마찬가지로 플레이어가 소유할 수 없는 물품인 것이다.

“에효, 정말이지 퀘템 말고는 아무것도 건질 게 없네. 세 달 동안 쓴 물약 값이 얼만데.”

나는 손에 든 책을 물끄러미 바라보았다.

‘어차피 아슈르에게 갖다 바쳐야 할 아이템인데 굳이 비싼 돈 들여 가며 감정해 볼 필요가 있을까?’

고민하던 나는 결국 플라리안의 눈을 꺼내 들었다.

세 달 동안이나 나를 고생시킨 근원의 정체가 무엇인지 궁금한 것은 당연한 이치였으니까.

“감정.”



<파그마의 기서> 

등급:레전드리

인간의 경지를 초월한 대장장이 장인 파그마의 기술이 집대성되어 있는 서적입니다. 책을 펼치는 순간, 어떠한 범인일지라도 전설의 대장장이가 될 수 있습니다.

효과:파그마의 후예로 전직.

조건:없음.

*사용 시 레벨과 능력치가 변동됩니다. 



[레전드리 아이템을 발견하였습니다!]

[대륙 전역에 명성이 500 상승합니다.]



몸이 부들부들 떨린다.

“헐… 대박…….”

과연 레전드리 아이템! 

발견자라는 이유만으로 대륙 전역에 명성이 무려 500이나 오르다니! 

일개 도시 안에서조차 명성 100 쌓기가 상당히 힘든 일이라는 점을 감안하면 이는 굉장한 수확이었다. 

‘명성도 명성이지만…….’

나는 내가 잘못 본 건 아닌지 의심해 보면서 아이템 설명을 다시 한 번 읽어 보았다. 그러나 다시 읽어도 내용에 변화는 없었다. 

“대~~ 박!!”

내가 헛것을 본 것이 아니었다. 

극도로 흥분한 탓에 머리가 띵하고 두근두근거리는 심장 소리가 귀까지 들려왔다.

기서라기에 단지 스킬북인 줄 알았더니 전직서라니? 

게다가 레전드리 등급의 전직서라니! 유일한 최강의 직업을 가질 수 있게 해 준다는 뜻이 아닌가!

“더군다나 사용 조건조차 없어…….”

주르륵, 눈물이 흘러내렸다.

대출 이자랑 Satisfy 계정비 벌겠답시고 학교도 휴학하고 인력소를 전전해 온 지난 1년을 회상해 보았다.

친구들이 하나둘씩 떠나고, 동창들은 비웃고, 주변인들에게는 괄시를 당하고, 스스로 생각하기에도 한심하고, 노가다 뛰다 보니 몸은 상하고…….

당초 계획은 게임하면서 얻게 되는 아이템들을 현금으로 팔아서 대출비와 계정비, 그리고 학비까지 전부 충당하는 것이었지만, 이 Satisfy가 그리 만만한 세계가 아니었다. 

돈 벌기가 워낙 힘들어서 아이템을 팔아 치울 여유는커녕 내 장비 맞추기도 어려운 실정이었다.

하지만 이제는 다르다.

전율이 일면서 전신이 부들부들 떨렸다.

“끝났어……. 이 악몽 같은 인생과도 이제 작별이다!”

조건 없는 레전드리 전직서!

아이템 거래 사이트에 경매 물품으로 등록하는 순간, 그 거래 가격이 순식간에 수천만 원을 호가할 것이 분명했다.

아니, 20억 명이 넘는 유저 중에서 유일한 최강의 직업을 갖게 해 주는 아이템인데 ‘고작’ 수천만 원밖에 안 할까? 최소 수억 원이 넘는 가치라고 확신할 수 있다. 어쩌면, 나 같은 놈은 상상조차 못 할 천문학적 금액을 손아귀에 쥘 수도!

“푸하하하하핫!! 어머니! 아버지! 밥만 축내던 아들놈이 드디어 해냈습니다! 이제는 게임 관두고 취직하라며 등짝 때리지 않으셔도 됩니다! 동네 창피하다고 아들놈 하나 없는 셈 치겠다는 술주정도 그만두셔도 됩니다! 세희야! 오빠가 드디어 해냈다! 이제 쪽팔린다고 길에서 마주칠 때마다 쌩까지 않아도 돼! 네 친구들이 집에 놀러 온다고 할 때마다 온갖 핑계 대면서 거절하지 않아도 된다고! 그리고 내 친구들아! 동창들아! 더 이상 나를 한심한 게임 폐인, 인생 쪽 난 놈이라고 무시하지 마라! 난 게임으로 성공했다! 고작 해 봐야 사회 초년생인 너희들보다 내가 몇 걸음이나 앞선 거라고! 푸하하하핫!!”

캡슐 구입비를 마련하느라 대출받았던 1천만 원과, 대출금 제때 못 갚은 바람에 매달 수십만 원씩 불어나는 이자와도 이제 안녕일지니!

‘아영이는 여전히 예쁘려나…….’

나는 2년째 참석하지 않았던 고등학교 동창회에 외제차를 끌고 등장하는 상상을 해 보았다.

성공한 나를 더 이상 무시하지 못하는 동창들. 그리고 내 첫사랑 아영이의 얼굴에 홍조가 그려지는 모습이 자연스럽게 떠올랐다.

“좋아, 어서 갖다 팔자!!”

퀘스트? 이제 그딴 건 내 알 바 아니다.

분명, 태양의 검은 에픽 아이템 중에서도 상급에 속하는 무기였다. 하지만 이 전직서에 비할 가치가 못 됐다.

아슈르 백작과의 호감도가 하락할 테지만, 말 시키면 무시하고 줘야 할 퀘스트 안 주는 정도의 반동만이 생길 터. 수억 원의 현금이 걸린 마당에 두려워할 이유가 하등 없었다. 

“로그아웃!”

나는 당당하게 외쳤다.

그리고 눈앞으로 알림창이 떠올랐다.



[이곳에서는 게임을 종료할 수 없습니다.]

[아슈르 백작이 출현합니다.]



“……?”

이해하지 못하고 멀뚱멀뚱 있자니 수십 명의 기사들이 동굴 안으로 뛰어 들어왔다. 그리고 뒤따라 낯익은 아슈르 백작이 등장했다.

당황하는 나를 발견한 그가 일그러진 표정으로 말했다.

“어리석은 여행자여, 같잖은 욕심을 품었구나.”



[퀘스트 <아슈르 백작의 은밀한 부탁>(S)이 <아슈르 백작의 분노>(SS)로 변경됩니다.]



<아슈르 백작의 분노> 

난이도:SS

적당한 능력이 있고 멍청해서 이용하기 쉬워 보이는 당신을 골라, ‘실존하는지 확실치도 않은’ 파그마의 기서를 찾아오라는 얼토당토않은 의뢰를 맡겼던 아슈르 백작. 

혹시나 하는 마음으로 당신에게 감시자를 붙였던 그는 당신이 ‘북쪽 끝의 동굴’을 발견했다는 소식을 접하자마자 직접 이곳까지 행차했다. 

욕심에 눈이 멀어 파그마의 기서를 빼돌리려 한 당신을 목격한 그는 당신을 용서할 생각이 없다. 당신을 살해하고 파그마의 기서를 빼앗아 갈 작정이다.

*아슈르 백작과의 호감도가 -100으로 하락했습니다.

*신의를 저버린 행동 탓에 파트리안에서 쌓아 온 모든 명성이 사라지고 악명이 높아졌습니다. 파트리안의 모든 주민들과의 호감도가 -40으로 하락했습니다. 그들은 당신을 보면 도둑놈이라고 야유할 것입니다.

퀘스트 클리어 조건:아슈르 백작과 호위 기사들의 전멸.

클리어 보상:칭호 ‘귀족 살해자’ 획득.

*귀족 살해자:지력 -50 
...
"""

data = {
    "title": "템빨",
    "content": novel_content,
    "author": "템빨작가"
}

response = requests.post(
    url,
    json=data,
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print("Response:")
print(response.json())

# 703