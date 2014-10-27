function RconConsole() {
    this.historyCache = {};
    this.activeServer = "";
    this.currentHistoryIndex = -1;
    
    this.history = function() {
        return this.historyCache[this.activeServer];
    }
    
    this.pushHistory = function(command) {
        // enqueue
        var h = this.history();
        h.unshift(command);
        this.currentHistoryIndex = -1;
    }
    
    this.up = function() {
        var h = this.history();
        console.log(h);
        console.log(this.currentHistoryIndex);
        if (this.currentHistoryIndex >= h.length - 1) {
            return null;
        } else {
            return h[++this.currentHistoryIndex];
        }
    }
    
    this.down = function() {
        var h = this.history();
        if (this.currentHistoryIndex <= 0) {
            this.currentHistoryIndex = -1;
            return null;
        } else {
            return h[--this.currentHistoryIndex];
        }
    }
    
    this.getActiveServer = function() {
        return this.activeServer;
    }
    
    this.setActiveServer = function(server) {
        this.activeServer = server;
        if (server in this.historyCache == false) {
            this.historyCache[server] = [];
        }
    }
}

var RCON_CONSOLE = new RconConsole();

$('.console-header > .row > div').not('.form').click(function() {
    var $console = $(this).parents('.console');
    var $header = $console.find('.console-header');
    
    // Going up Kappa
    if ($header.find('span').hasClass('glyphicon-chevron-up')) {
        $console.animate({'height': '60%'}, 500);
    } else {
        $console.animate({'height': '3em'}, 500);
    }
    
    $header.find('span').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
});

$('.console input').keyup(function(e){
    if (e.keyCode == 13) {
        $(this).trigger('enterKey');
    } else if (e.keyCode == 38) {
        $(this).trigger('upArrow');
    } else if (e.keyCode == 40) {
        $(this).trigger('downArrow');
    }
});

$('.console-body input').on('enterKey', function() {
    var command = $(this).val();
    if ($.trim(command).length == 0) {
        $(this).val('');
        return;
    }
    var $console = $(this).parents('.console');
    var $textarea = $console.find('textarea:visible');
    $textarea.val($textarea.val() + '> ' + command + '\n');
    RCON_CONSOLE.pushHistory(command);
    $(this).val('');
    $.post('/command', {
        'server': RCON_CONSOLE.getActiveServer(),
        'command': command
    }, function(response) {
        if (response.success) {
            $textarea.val($textarea.val() + response.result.replace(/\x00/g, '') + '\n');
        } else {
            $textarea.val($textarea.val() + 'ERROR: ' + response.error + '\n');
        }
    }, 'json');
});

$('.console-body input').on('upArrow', function() {
    var hist = RCON_CONSOLE.up();
    if (hist != null) {
        $(this).val(hist);
    }
});

$('.console-body input').on('downArrow', function() {
    var hist = RCON_CONSOLE.down();
    if (hist != null) {
        $(this).val(hist);
    } else {
        $(this).val('');
    }
});

$('.console-header .form > select').change(function() {
    var $console = $(this).parents('.console');
    $console.find('textarea').hide();
    $console.find('textarea[data-server="%s"]'.replace('%s', $(this).val())).show();
    RCON_CONSOLE.setActiveServer($(this).val());
});
$('.console-header .form > select').change();