import QtQuick 2.15
import QtQuick.Controls 2.15
import QtLottie 1.0

Rectangle {
    width: 1080
    height: 1920
    color: "transparent"

    LottieAnimation {
        id: anim
        source: "animation.json"   // Remplace par ton fichier JSON
        anchors.fill: parent
        playing: true
        loops: LottieAnimation.Infinite
        autoPlay: true
    }
}