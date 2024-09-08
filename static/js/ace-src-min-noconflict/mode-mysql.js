ace.define("ace/mode/doc_comment_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],function(e,t,n){"use strict";var r=e("../lib/oop"),i=e("./text_highlight_rules").TextHighlightRules,s=function(){this.$rules={start:[{token:"comment.doc.tag",regex:"@\\w+(?=\\s|$)"},s.getTagRule(),{defaultToken:"comment.doc.body",caseInsensitive:!0}]}};r.inherits(s,i),s.getTagRule=function(e){return{token:"comment.doc.tag.storage.type",regex:"\\b(?:TODO|FIXME|XXX|HACK)\\b"}},s.getStartRule=function(e){return{token:"comment.doc",regex:/\/\*\*(?!\/)/,next:e}},s.getEndRule=function(e){return{token:"comment.doc",regex:"\\*\\/",next:e}},t.DocCommentHighlightRules=s}),ace.define("ace/mode/mysql_highlight_rules",["require","exports","module","ace/lib/oop","ace/lib/lang","ace/mode/doc_comment_highlight_rules","ace/mode/text_highlight_rules"],function(e,t,n){var r=e("../lib/oop"),i=e("../lib/lang"),s=e("./doc_comment_highlight_rules").DocCommentHighlightRules,o=e("./text_highlight_rules").TextHighlightRules,u=function(){function l(e){var t=e.start,n=e.escape;return{token:"string.start",regex:t,next:[{token:"constant.language.escape",regex:n},{token:"string.end",next:"start",regex:t},{defaultToken:"string"}]}}var e="alter|and|as|asc|between|count|create|delete|desc|distinct|drop|from|lateral|having|in|insert|into|is|join|like|not|on|or|order|select|set|table|union|intersect|except|update|values|where|accessible|action|add|after|algorithm|all|analyze|asensitive|at|authors|auto_increment|autocommit|avg|avg_row_length|before|binary|binlog|both|btree|cache|call|cascade|cascaded|case|catalog_name|chain|change|changed|character|check|checkpoint|checksum|class_origin|client_statistics|close|code|collate|collation|collations|column|columns|comment|commit|committed|completion|concurrent|condition|connection|consistent|constraint|contains|continue|contributors|convert|cross|current_date|current_time|current_timestamp|current_user|cursor|data|database|databases|day_hour|day_microsecond|day_minute|day_second|deallocate|dec|declare|default|delay_key_write|delayed|delimiter|des_key_file|describe|deterministic|dev_pop|dev_samp|deviance|directory|disable|discard|distinctrow|div|dual|dumpfile|each|elseif|enable|enclosed|end|ends|engine|engines|enum|errors|escape|escaped|even|event|events|every|execute|exists|exit|explain|extended|fast|fetch|field|fields|first|flush|for|force|foreign|found_rows|full|fulltext|function|general|global|grant|grants|group|by|group_concat|handler|hash|help|high_priority|hosts|hour_microsecond|hour_minute|hour_second|if|ignore|ignore_server_ids|import|index|index_statistics|infile|inner|innodb|inout|insensitive|insert_method|install|interval|invoker|isolation|iterate|key|keys|kill|language|last|leading|leave|left|level|limit|linear|lines|list|load|local|localtime|localtimestamp|lock|logs|low_priority|master|master_heartbeat_period|master_ssl_verify_server_cert|masters|match|max|max_rows|maxvalue|message_text|middleint|migrate|min|min_rows|minute_microsecond|minute_second|mod|mode|modifies|modify|mutex|mysql_errno|natural|next|no|no_write_to_binlog|offline|offset|one|online|open|optimize|option|optionally|out|outer|outfile|pack_keys|parser|partition|partitions|password|phase|plugin|plugins|prepare|preserve|prev|primary|privileges|procedure|processlist|profile|profiles|purge|query|quick|range|read|read_write|reads|real|rebuild|recover|references|regexp|relaylog|release|remove|rename|reorganize|repair|repeatable|replace|require|resignal|restrict|resume|return|returns|revoke|right|rlike|rollback|rollup|row|row_format|rtree|savepoint|schedule|schema|schema_name|schemas|second_microsecond|security|sensitive|separator|serializable|server|session|share|show|signal|slave|slow|smallint|snapshot|soname|spatial|specific|sql|sql_big_result|sql_buffer_result|sql_cache|sql_calc_found_rows|sql_no_cache|sql_small_result|sqlexception|sqlstate|sqlwarning|ssl|start|starting|starts|status|std|stddev|stddev_pop|stddev_samp|storage|straight_join|subclass_origin|sum|suspend|table_name|table_statistics|tables|tablespace|temporary|terminated|to|trailing|transaction|trigger|triggers|truncate|uncommitted|undo|uninstall|unique|unlock|upgrade|usage|use|use_frm|user|user_resources|user_statistics|using|utc_date|utc_time|utc_timestamp|value|variables|varying|view|views|warnings|when|while|with|work|write|xa|xor|year_month|zerofill|begin|do|then|else|loop|repeat",t="rank|coalesce|ifnull|isnull|nvl",n="charset|clear|connect|edit|ego|exit|go|help|nopager|notee|nowarning|pager|print|prompt|quit|rehash|source|status|system|tee",r="adddate|addtime|convert_tz|curdate|current_date|current_time|current_timestamp|curtime|date|date_add|date_format|date_sub|datediff|day|dayname|dayofmonth|dayofweek|dayofyear|extract|from_days|from_unixtime|get_format|hour|last_day|localtime|localtimestamp|makedate|maketime|microsecond|minute|month|monthname|now|period_add|period_diff|quarter|sec_to_time|second|str_to_date|subdate|subtime|sysdate|time|time_format|time_to_sec|timediff|timestamp|timestampadd|timestampdiff|to_days|to_seconds|unix_timestamp|utc_date|utc_time|utc_timestamp|week|weekday|weekofyear|year|yearweek",i="aes_decrypt|aes_encrypt|compress|md|random_bytes|sha|sha|statement_digest|statement_digest_text|uncompress|uncompressed_length|validate_password_strength",o="abs|acos|asin|atan|atan|ceil|ceiling|conv|cos|cot|crc|degrees|div|exp|floor|ln|log|log10|log2|mod|pi|pow|power|radians|rand|round|sign|sin|sqrt|tan|truncate",u="ascii|bin|bit_length|char|char_length|character_length|concat|concat_ws|elt|export_set|field|find_in_set|format|from_base|hex|insert|instr|lcase|left|length|like|load_file|locate|lower|lpad|ltrim|make_set|match|mid|not|not|oct|octet_length|ord|position|quote|regexp|regexp_instr|regexp_like|regexp_replace|regexp_substr|repeat|replace|reverse|right|rlike|rpad|rtrim|soundex|sounds|space|strcmp|substr|substring|substring_index|to_base|trim|ucase|unhex|upper|weight_string",a="bool|boolean|bit|blob|decimal|double|enum|float|long|longblob|longtext|medium|mediumblob|mediumint|mediumtext|time|timestamp|tinyblob|tinyint|tinytext|text|bigint|int|int1|int2|int3|int4|int8|integer|float|float4|float8|double|char|varbinary|varchar|varcharacter|precision|date|datetime|year|unsigned|signed|numeric",f=this.createKeywordMapper({"support.function":[t,r,i,o,u].join("|"),keyword:e,"storage.type":a,constant:"false|true|null|unknown|ODBCdotTable|zerolessFloat","variable.language":n},"identifier",!0);this.$rules={start:[{token:"comment",regex:"(?:-- |#).*$"},l({start:'"',escape:/\\[0'"bnrtZ\\%_]?/}),l({start:"'",escape:/\\[0'"bnrtZ\\%_]?/}),s.getStartRule("doc-start"),{token:"comment",regex:/\/\*/,next:"comment"},{token:"constant.numeric",regex:/0[xX][0-9a-fA-F]+|[xX]'[0-9a-fA-F]+'|0[bB][01]+|[bB]'[01]+'/},{token:"constant.numeric",regex:"[+-]?\\d+(?:(?:\\.\\d*)?(?:[eE][+-]?\\d+)?)?\\b"},{token:f,regex:"[a-zA-Z_$][a-zA-Z0-9_$]*\\b"},{token:"constant.class",regex:"@@?[a-zA-Z_$][a-zA-Z0-9_$]*\\b"},{token:"constant.buildin",regex:"`[^`]*`"},{token:"keyword.operator",regex:"\\+|\\-|\\/|\\/\\/|%|<@>|@>|<@|&|\\^|~|<|>|<=|=>|==|!=|<>|="},{token:"paren.lparen",regex:"[\\(]"},{token:"paren.rparen",regex:"[\\)]"},{token:"text",regex:"\\s+"}],comment:[{token:"comment",regex:"\\*\\/",next:"start"},{defaultToken:"comment"}]},this.embedRules(s,"doc-",[s.getEndRule("start")]),this.normalizeRules()};r.inherits(u,o),t.MysqlHighlightRules=u}),ace.define("ace/mode/mysql",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/mysql_highlight_rules"],function(e,t,n){var r=e("../lib/oop"),i=e("../mode/text").Mode,s=e("./mysql_highlight_rules").MysqlHighlightRules,o=function(){this.HighlightRules=s,this.$behaviour=this.$defaultBehaviour};r.inherits(o,i),function(){this.lineCommentStart=["--","#"],this.blockComment={start:"/*",end:"*/"},this.$id="ace/mode/mysql"}.call(o.prototype),t.Mode=o});                (function() {
                    ace.require(["ace/mode/mysql"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            