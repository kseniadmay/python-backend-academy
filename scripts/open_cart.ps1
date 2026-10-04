$opera = "C:\Users\fury6\AppData\Local\Programs\Opera Air\opera.exe"
$urls = @(
    "https://myspar.ru/catalog/polufabrikaty-1/shnitsel-po-ministerski-/",
    "https://myspar.ru/catalog/kashi-gotovye-zavtraki/kasha-ovsyanaya-bystrov-prebio-assorti-slivki-240-g/",
    "https://myspar.ru/catalog/lepeshki-lavash-syr-dlya-grilya/lavash-armyanskiy-tonkiy-s-aromatom-syra-dlya-proizvodstva/",
    "https://myspar.ru/catalog/moloko/moloko-ultrapasterizovannoe-2-5-spar-1000ml/",
    "https://myspar.ru/catalog/molochnaya-produktsiya/syr-maasdam-45-premium-spar/",
    "https://myspar.ru/catalog/supertsena/kapusta-pekinskaya-we-love-fresh/",
    "https://myspar.ru/catalog/ovoshchi/ogurtsy-korotkoplodnye/",
    "https://myspar.ru/catalog/ovoshchi/tomat-rozovyy-1/",
    "https://myspar.ru/catalog/supertsena/perets-sovkhoznyy/",
    "https://myspar.ru/catalog/ovoshchi/morkov-sladkaya-senkino-1kg/",
    "https://myspar.ru/catalog/frukty/banany/",
    "https://myspar.ru/catalog/frukty/yabloki-novyy-urozhay/",
    "https://myspar.ru/catalog/frukty/mandariny/",
    "https://myspar.ru/catalog/supertsena/vinograd-teffi/"
)

foreach ($url in $urls) {
    Start-Process $opera $url
    Start-Sleep -Milliseconds 400
}
