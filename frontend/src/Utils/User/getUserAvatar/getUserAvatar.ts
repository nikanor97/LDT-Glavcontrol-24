
import {sum, round} from 'lodash';
import a1 from './images/image1.svg';
import a2 from './images/image2.svg';
import a3 from './images/image3.svg';
import a4 from './images/image4.svg';
import a5 from './images/image5.svg';
import a6 from './images/image6.svg';
import a7 from './images/image7.svg';
import a8 from './images/image8.svg';
import a9 from './images/image9.svg';
import a10 from './images/image10.svg';
import {StaticImageData} from 'next/image';

const images = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10] as StaticImageData[];


export const getUserAvatar = (uid: string) => {
    const lettersSum = sum(
        uid
            .split('')
            .map((letter) => letter.charCodeAt(0))
    )
    const ost = lettersSum % 100;
    const resultIndex = round((ost / 100) * (images.length - 1))
    return images[resultIndex];
}