    let securedDivs = document.querySelectorAll('.secured-button > div') , gk;

    for(gk=0; gk< securedDivs.length; gk++){
        let divStyle = getComputedStyle(securedDivs[gk]);

        if(
            divStyle.opacity == 1 &&
            divStyle.display != 'none' &&
            divStyle.height != 0 &&
            divStyle.visibility != 'hidden' &&
            divStyle.transform != 'matrix(1, 0, 0, 1, 9999, 0)' &&
            (divStyle.getPropertyValue("z-index") === '1' ||  divStyle.getPropertyValue("z-index") === 'auto') &&
            divStyle.position != 'absolute'
        ){
            return(securedDivs[gk].classList);
        }
     }
